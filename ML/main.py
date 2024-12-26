from fastapi import FastAPI, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from src.read_data import SimpleCompactData
from src.recommender import Simple_Recommender
from src.scheduler import DataUpdateScheduler
import uvicorn
import logging
import os
import ssl
from dotenv import load_dotenv

load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# ssl_context.load_cert_chain(
#     os.getenv("CERT_PATH"),
#     keyfile=os.getenv("KEY_PATH")
# )


data: SimpleCompactData | None = None
recommender: Simple_Recommender | None = None
scheduler: DataUpdateScheduler | None = None


async def initialize_system():
    """
    Инициализирует данные и рекомендательную систему.
    """
    global data, recommender, scheduler

    data = SimpleCompactData()
    await data.load_data()
    data.data_preprocessing()
    logger.info("Data successfully loaded and preprocessed.")

    recommender = Simple_Recommender(data)
    logger.info("Recommender system initialized.")

    # Инициализация и запуск планировщика
    scheduler = DataUpdateScheduler(data, recommender)
    scheduler.start()
    logger.info("Data update scheduler started.")


# @app.on_event("startup")
# async def startup_event():
#     """
#     Выполняется при запуске приложения.
#     """
#     FastAPICache.init(InMemoryBackend())
#     await initialize_system()


@app.on_event("shutdown")
async def shutdown_event():
    """
    Выполняется при остановке приложения.
    """
    if scheduler:
        scheduler.stop()
        logger.info("Scheduler stopped during shutdown.")


@app.get("/recommendations/user/{user_id}")
@cache(expire=3600)
async def recommend_user(user_id: int, neighbours: int = 1, films: int = 10):
    """
    Рекомендует фильмы для пользователя.
    """
    try:
        recommendations = await recommender.get_user_recommendations(user_id, neighbours, films)
        return {"user_id": user_id, "recommendations": recommendations}
    except Exception as e:
        raise HTTPException(
            status_code=422, detail=f"Error generating recommendations: {e}")


@app.get("/recommendations/movie/{movie_id}")
@cache(expire=3600)
async def recommend_movie(movie_id: int, k: int = 10):
    """
    Рекомендует похожие фильмы.
    """
    try:
        recommendations = recommender.get_movie_recommendations(movie_id, k)
        return {"movie_title": movie_id, "recommendations": recommendations}
    except Exception as e:
        raise HTTPException(
            status_code=422, detail=f"Error generating movie recommendations: {e}")


@app.post("/admin/reload")
async def reload_system():
    """
    Перезагружает данные и модель.
    """
    try:
        await initialize_system()
        return {"message": "System reloaded successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=422, detail=f"Error reloading system: {e}")


@app.get("/admin/status")
async def system_status():
    """
    Возвращает статус системы.
    """
    try:
        return {
            "data_loaded": (data is not None),
            "model_loaded": (recommender is not None),
            "total_users": len(data.user_mapper) if isinstance(data, SimpleCompactData) else 0,
            "total_movies": len(data.movie_mapper) if isinstance(data, SimpleCompactData) else 0
        }
    except Exception as e:
        raise HTTPException(
            status_code=422, detail=f"Error fetching system status: {e}")


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
        "/help": "Provides information about available endpoints"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
