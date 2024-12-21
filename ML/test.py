from fastapi import FastAPI, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from src.read_data import CompactData
from src.recommender import Simple_Recommender
from src.repository import Repository
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


data = None
recommender = None

async def initialize_system():
    """
    Инициализирует данные и рекомендательную систему.
    """
    global data, recommender

    data = CompactData()
    await data.load_data()
    data.data_preprocessing()
    logger.info("Data successfully loaded and preprocessed.")

    recommender = Simple_Recommender(data)
    logger.info("Recommender system initialized.")

@app.on_event("startup")
async def startup_event():
    """
    Выполняется при запуске приложения.
    """
    FastAPICache.init(InMemoryBackend())
    await initialize_system()

@app.get("/recommendations/user/{user_id}")
@cache(expire=3600)
async def recommend_user(user_id: int, neighbours: int = 1, films: int = 10):
    """
    Рекомендует фильмы для пользователя.
    """
    try:
        recommendations = await recommender.get_user_recommendations(user_id, neighbours, films)
        if not recommendations:
            raise HTTPException(status_code=404, detail="No recommendations found.")
        return {"user_id": user_id, "recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {e}")

@app.get("/recommendations/movie/{movie_title}")
@cache(expire=3600)
async def recommend_movie(movie_id: int, k: int = 10):
    """
    Рекомендует похожие фильмы.
    """
    try:
        recommendations = recommender.get_movie_recommendations(movie_id, k)
        if not recommendations:
            raise HTTPException(status_code=404, detail=f"No similar movies found for '{movie_id}'.")
        return {"movie_title": movie_id, "recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating movie recommendations: {e}")

@app.post("/admin/reload")
async def reload_system():
    """
    Перезагружает данные и модель.
    """
    try:
        await initialize_system()
        return {"message": "System reloaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reloading system: {e}")

@app.get("/admin/status")
async def system_status():
    """
    Возвращает статус системы.
    """
    try:
        return {
            "data_loaded": (data is not None),
            "model_loaded": (recommender is not None),
            "total_users": len(data.user_mapper) if isinstance(data, CompactData) else 0,
            "total_movies": len(data.movie_mapper) if isinstance(data, CompactData) else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching system status: {e}")

@app.get("/help")
async def help():
    """
    Возвращает информацию о доступных эндпоинтах.
    """
    return {
        "/recommendations/user/{user_id}": "Recommends movies for a given user",
        "/recommendations/movie/{movie_title}": "Recommends similar movies",
        "/admin/reload": "Reloads the system",
        "/admin/status": "Returns system status",
        "/admin/save_data": "Saves preprocessed data",
        "/admin/clear_data": "Clears preprocessed data",
        "/help": "Provides information about available endpoints"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)