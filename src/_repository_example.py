from repository.scores import ScoreRepo
from repository.users import UserRepo
from repository.movies import MovieRepo
import asyncio


async def main():
    user_repo = UserRepo()
    movie_repo = MovieRepo()
    score_repo = ScoreRepo()

    users = await user_repo.get_all()
    print('Users:')
    for u in users:
        print(u.user_id, u.login, u.watched_movies, u.scores)
    print('\n')

    movies = await movie_repo.get_all()
    print('Movies:')
    for m in movies:
        print(m.movie_id, m.name, m.preview, m.file, m.watched_by, m.scores)
    print('\n')

    scores = await score_repo.get_all()
    print('Scores:')
    for s in scores:
        print(s.user, s.movie, s.score)
    print('\n')


asyncio.run(main())
