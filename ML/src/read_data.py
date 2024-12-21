import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from src.repository import Repository


class CompactData:

    """
    Class representing compact data for recommendation system.
    """

    def __init__(self):
        """
        Initializes the CompactData object.
        """
        self.user_mapper = None
        self.movie_mapper = None
        self.index_movie = None
        self.df = None
        self.user_item_matrix = None
        self.repo = Repository()

    async def load_data(self):
        """Loads raw data from Database."""
        self.df = pd.DataFrame(await self.repo.get_all(), columns=['userId', 'movieId', 'rating'])

    def data_preprocessing(self):
        """Preprocesses data to create mappings and user-item matrix."""
        users = self.df['userId'].unique()
        movies = self.df['movieId'].unique()

        self.user_mapper = {user: i for i, user in enumerate(users)}
        self.movie_mapper = {movie: i for i, movie in enumerate(movies)}
        self.index_movie = {i: movie for i, movie in enumerate(movies)}

        self.df['user_index'] = self.df['userId'].map(self.user_mapper)
        self.df['movie_index'] = self.df['movieId'].map(self.movie_mapper)

        # Ensure ratings are converted to np.int16
        ratings = self.df['rating'].astype(np.int16)

        self.user_item_matrix = csr_matrix(
            (ratings, (self.df['user_index'], self.df['movie_index'])),
            shape=(len(users), len(movies)),
            dtype=np.int16
        )

    async def get_watched_ids(self, user_id):
        """Возвращает список индексов просмотренных фильмов для данного пользователя."""
        movie_ids = await self.repo.get_watched(user_id)
        # Преобразуем ID фильмов в индексы матрицы через movie_mapper
        watched_indices = [self.movie_mapper[movie_id] for movie_id in movie_ids]
        return watched_indices

    def getcol(self, col):
        """Returns a specific column from the user-item matrix."""
        return self.user_item_matrix.getcol(col)

    def toarray(self):
        """Converts the user-item matrix to a dense array."""
        return self.user_item_matrix.toarray()

    def getrow(self, row):
        """Returns a specific row from the user-item matrix."""
        return self.user_item_matrix.getrow(row)
