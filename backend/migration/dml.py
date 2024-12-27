from src.repository.users import UserRepo, User
from src.repository.movies import MovieRepo, Movie
from src.repository.scores import ScoreRepo, Score
import pandas as pd
import asyncio

user_repo = UserRepo()
movie_repo = MovieRepo()
score_repo = ScoreRepo()


async def add_users():
    user_df = pd.read_csv(
        '/Users/timursalihov/Python_project/users_v2_shorter.csv')

    for _, row in user_df.iterrows():
        u = User()
        u.user_id = row['user_id']
        u.role = row['role']

        await user_repo.add(u)
        print(f"Added user_id: {row['user_id']}")


async def add_movies():
    movie_df = pd.read_csv(
        '/Users/timursalihov/Python_project/movies_shorter.csv')

    for _, row in movie_df.iterrows():
        m = Movie()
        m.movie_id = row['movie_id']
        m.name = row['title']
        m.genres = eval(row['genres'])
        m.year = row['year']
        m.preview = row['preview']
        m.file = row['file']

        await movie_repo.add(m)
        print(f"Added movie_id: {row['movie_id']}")


async def add_watched():
    watched_df = pd.read_csv(
        '/Users/timursalihov/Python_project/watched_shorter.csv')

    for _, row in watched_df.iterrows():
        await user_repo.add_watched(row['user_id'], row['movie_id'])
        print(f"User {row['user_id']} watched {row['movie_id']}")


async def add_scores():
    scores_df = pd.read_csv(
        '/Users/timursalihov/Python_project/new_rating_shorter.csv')

    for _, row in scores_df.iterrows():
        await score_repo.add_score(row['user_id'], row['movie_id'], row['rating'])
        print(f"User {row['user_id']} has set movie {
              row['movie_id']} a score of {row['rating']}")


async def main():
    await add_scores()


if __name__ == "__main__":
    asyncio.run(main())
