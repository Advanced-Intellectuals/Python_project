from types import new_class

from fastapi import HTTPException
from repository.scores import ScoreRepo, Score

class ScoreService:
    def __init__(self, score_repo: ScoreRepo):
        self.score_repo = score_repo

    async def add_score_to_movie(self, user_id, movie_id, score):

        result = await self.score_repo.add_score(user_id, movie_id, float(score / 2))

        return result