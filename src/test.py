from repository.scores import ScoreRepo
import asyncio


async def main():
    repo = ScoreRepo()
    res = await repo.get_all()

    for s in res:
        print(s)

asyncio.run(main())
