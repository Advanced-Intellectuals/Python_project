from src.read_data import CompactData
from src.recommender import Simple_Recommender
import asyncio as asy

async def main():
    data = CompactData()
    await data.load_data()
    data.data_preprocessing()
    k = Simple_Recommender(data)
    a = k.get_movie_recommendations(2)
    print(a)

# print(Simple_Recommender(data).get_user_recommendations(1, 10, 5))
asy.run(main())

# print(Simple_Recommender(data).get_movie_recommendations(2))