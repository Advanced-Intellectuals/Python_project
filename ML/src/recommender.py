from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from src.read_data import CompactData

class Simple_Recommender:

    """
    Recommends movies to users based on their ratings and the ratings of their k-nearest neighbors.
    """

    def __init__(self, data:CompactData):
        self.data = data

    def get_user_ratings(self, user_id):
        """
          Retrieves the array of ratings for a specific user from the user_item_matrix.

          Args:
            user_id: The ID of the user whose ratings are to be retrieved.

          Returns:
            A NumPy array of ratings for the specified user, or None if the user is not found.
          """
        try:
            # user_index = np.int16(self.data.user_mapper[user_id])
            user_index = user_id
            return self.data.getrow(user_index).toarray()[0].astype(np.float16)
        except KeyError:
            print(f"User with ID {user_id} not found.")
            return None
        except Exception as e:
            print(f"Unexpected error in 'get_user_ratings': {e}")
            return None

    def get_k_nearest_neighbors(self, user_id, k=10, user_ratings=False):
        """
        Retrieves the k nearest neighbors for a specific user based on the cosine similarity of their ratings.

        Parameters:
            user_id (int): ID of the target user.
            k (int): Number of nearest neighbors to retrieve. Use -1 to retrieve all neighbors.
            user_ratings (numpy.ndarray): Optional precomputed ratings vector for the user.

        Returns:
            tuple: (list of neighbor indices, list of similarity scores)
        """
        try:
            # Get user ratings if not provided
            if user_ratings is False:
                user_ratings = self.get_user_ratings(user_id)
                if user_ratings is None:
                    return None, None

            # Compute cosine similarity between the target user and all users
            similarity_scores = cosine_similarity(self.data.user_item_matrix, user_ratings.reshape(1, -1)).flatten().astype(np.float32)

            # Exclude the user themselves from the neighbor list
            # similarity_scores[self.data.user_mapper[user_id]] = -2
            similarity_scores[user_id] = -2

            if k > len(self.data.user_mapper): k = len(self.data.user_mapper) - 1

            # Get the indices of the top-k most similar users
            nearest_neighbors = similarity_scores.argsort()[::-1][:k]
            top_k_scores = similarity_scores[nearest_neighbors]

            return nearest_neighbors.astype(np.int32), top_k_scores

        except KeyError:
            print(f"Error: User with ID {user_id} not found in user_mapper.")
            return None, None
        except ValueError as e:
            print(f"ValueError in 'get_k_nearest_neighbors': {e}")
            return None, None
        except Exception as e:
            print(f"Unexpected error in 'get_k_nearest_neighbors': {e}")
            return None, None

    async def get_user_recommendations(self, user_id, neighbours=25, films=24):
        """
        Recommends movies to a user based on the ratings of their k-nearest neighbors,
        using a weighted average approach where weights are based on similarity.

        Parameters:
            user_id (int): ID of the user to recommend movies for.
            neighbours (int): Number of nearest neighbors to consider.
            films (int): Number of recommended movies to return. Use -1 to return all.

        Returns:
            list: List of recommended movie titles.
        """
        try:
            tmp = user_id
            user_id = self.data.user_mapper.get(user_id, None)

            if user_id is None:
                movie_popularity = self.data.df.groupby('movieId')['rating'].mean().sort_values(ascending=False)
                recommended_movies = movie_popularity.index.tolist()
                return recommended_movies[:films]

            # Get user ratings
            user_ratings = self.get_user_ratings(user_id)

            # Find nearest neighbors
            nearest_neighbors, similarity_scores = self.get_k_nearest_neighbors(user_id, neighbours, user_ratings)
            if nearest_neighbors is None or len(nearest_neighbors) == 0:
                raise ValueError(f"No nearest neighbors found for user ID {user_id}.")

            # Extract neighbors' ratings and apply similarity-based weighting
            neighbor_ratings = self.data.user_item_matrix[nearest_neighbors].toarray()
            similarity_scores = np.array(similarity_scores).reshape(-1, 1)  # Reshape for matrix multiplication

            # Compute weighted sum of ratings and normalize by similarity scores
            weighted_ratings = np.dot(similarity_scores.T, neighbor_ratings).flatten()
            average_neighbor_ratings = weighted_ratings / np.sum(similarity_scores)

            # Identify movies the user hasn't rated
            # user_rated_movies = self.data.user_item_matrix[self.data.user_mapper[user_id]].nonzero()[1]
            user_rated_movies = await self.data.get_watched_ids(tmp)
            unrated_movies = np.setdiff1d(np.arange(len(self.data.movie_mapper)), user_rated_movies)

            # Sort movies by weighted average ratings
            unrated_ratings = average_neighbor_ratings[unrated_movies]
            recommended_movie_indices = np.argsort(-unrated_ratings)  # Descending order
            recommended_movies = [self.data.index_movie[idx] for idx in recommended_movie_indices]

            if films > len(self.data.movie_mapper): films = len(self.data.movie_mapper)

            return recommended_movies[:films]

        except ValueError as e:
            print(f"ValueError in 'get_user_recommendations': {e}")
            return []
        except Exception as e:
            print(f"Unexpected error in 'get_user_recommendations': {e}")
            return []

    def get_movie_recommendations(self, movie_title, k=5):
        """Recommends similar movies based on movie title."""
        try:
            movie_index = self.data.movie_mapper[movie_title]
        except KeyError:
            print(f"Error: Movie '{movie_title}' not found.")
            return []

        try:
            # Use cosine similarity to find similar movies
            movie_similarity_scores = cosine_similarity(self.data.user_item_matrix.T, self.data.user_item_matrix.T[movie_index])
            movie_similarity_scores[movie_index] = -2

            if k > len(self.data.movie_mapper): k = len(self.data.movie_mapper) - 1

            similar_movies_indices = (movie_similarity_scores.flatten().argsort()[::-1])[:k]
            recommended_movies = [self.data.index_movie[i] for i in similar_movies_indices]

            return recommended_movies
        except Exception as e:
            print(f"Unexpected error in 'get_movie_recommendations': {e}")
            return []

class Modern_Recommender:
    pass