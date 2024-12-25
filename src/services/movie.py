from types import new_class

from fastapi import HTTPException
from repository.movies import MovieRepo, Movie

class MovieService:
    def __init__(self, movie_repo: MovieRepo):
        self.movie_repo = movie_repo

    async def main_movies(self, page_number, page_size, start_year, end_year, genres):
        movies = await self.movie_repo.get_page(page_number, page_size, start_year, end_year, genres)

        movies = [{"movie_id": movie.movie_id,
                   "name": movie.name,
                   "year": movie.year,
                   "file": movie.file,
                   "genres": movie.genres,
                   "preview": movie.preview} for movie in movies]

        return movies

    async def search_movies(self, searched_title):
        movies = await self.movie_repo.find(searched_title)

        return movies

    async def add_movie(self, name, genres, year, preview, file):

        new_movie = Movie()
        new_movie.name = name
        new_movie.genres = genres
        new_movie.year = year
        new_movie.preview = preview
        new_movie.file = file

        await self.movie_repo.add(new_movie)

    async def recommend_movies(self, ids: list[int]):
        movies = await self.movie_repo.get_by_ids(ids)

        return movies