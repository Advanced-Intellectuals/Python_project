from src.read_data import CompactData
from src.recommender import Simple_Recommender
import asyncio as asy

async def main():
    data = CompactData()
    await data.load_data()
    data.data_preprocessing()
    k = await Simple_Recommender(data).get_user_recommendations(1, 10, 5)
    print(k)

# print(Simple_Recommender(data).get_user_recommendations(1, 10, 5))
asy.run(main())