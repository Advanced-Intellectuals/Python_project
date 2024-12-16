import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import pickle
import os


class CompactData:

    """
    Class CompactData is a data structure to store a compact representation of the original data.
    It is used by the Recommender class to store the user-item matrix and the mapper dictionaries.
    """

    def __init__(self, path=None):
        """
        Initializes the CompactData object.

        Args:
            path (str): Path to the CSV file directory.
        """
        self.user_mapper = None
        self.movie_mapper = None
        self.index_movie = None
        self.df = None
        self.user_item_matrix = None
        self.path = path

    def load_data(self, path=None):
        """Loads raw data from the CSV file."""
        if path is None:
            path = self.path

        if path is None:
            raise ValueError("Path to the CSV file is not provided.")
        self.df = pd.read_csv(path, usecols=['userId', 'rating', 'movieId'])

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

    def save_preprocessed_data(self, path):
        """Saves preprocessed data to a file for fast future loading."""
        with open(path, 'wb') as f:
            pickle.dump((self.user_item_matrix, self.user_mapper, self.movie_mapper, self.index_movie, self.df), f)

    def load_preprocessed_data(self, path):
        """Loads preprocessed data from a file if it exists."""
        if os.path.exists(path):
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.user_mapper = data[1]#data['user_mapper']
                self.movie_mapper = data[2]#data['movie_mapper']
                self.index_movie = data[3]#data['index_movie']
                self.user_item_matrix = data[0]#data['user_item_matrix']
                self.df = data[4]#data['df']
            print(f"Preprocessed data loaded from {path}")
            return True
        return False

    def getcol(self, col):
        """Returns a specific column from the user-item matrix."""
        return self.user_item_matrix.getcol(col)

    def toarray(self):
        """Converts the user-item matrix to a dense array."""
        return self.user_item_matrix.toarray()

    def getrow(self, row):
        """Returns a specific row from the user-item matrix."""
        return self.user_item_matrix.getrow(row)
