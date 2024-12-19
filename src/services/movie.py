from fastapi import HTTPException
from repository.movies import MovieRepo

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