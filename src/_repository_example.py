from repository.scores import ScoreRepo
from repository.users import UserRepo, User
from repository.movies import MovieRepo, Movie
import asyncio


async def main():
    user_repo = UserRepo()
    movie_repo = MovieRepo()
    score_repo = ScoreRepo()

    # Examples of getting whole tables
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

    # Example of recieving a user by login
    user = await user_repo.get_by_login('tsalikhov')
    print(user.password_hash)

    # Example of adding a user to database
    user = User(login='eepifanov', password_hash='123',
                first_name='Eugene', email='epif@mai.ru')

    await user_repo.add(user)

    # Example of deleting user by login
    await user_repo.delete('eepifanov')

    # Example of movie lookup
    movie = await movie_repo.get_by_id(1)
    print(movie)

    # Example of adding movie
    movie = Movie(name='Avengers: Endgame', year=2019, genres=[
                  'action', 'drama'], preview='acde070d-8c4c-4f0d-9d8a-162843c10333', file='acde070d-8c4c-4f0d-9d8a-162843c10333')
    await movie_repo.add(movie)

    # Example of deleting a movie
    # await movie_repo.delete(2)

    # Example of marking a movie as watched for user
    await user_repo.add_watched(14, 1)

    # Example of adding a score from user to movie
    await score_repo.add_score(14, 1, 4.5)


asyncio.run(main())
