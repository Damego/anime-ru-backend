from pydantic import BaseModel

from .anime import Anime
from .user import User


class WatchType(BaseModel):
    id: int
    name: str


class AnimeRating(BaseModel):
    anime: Anime
    user: User
    score: int
    score_by_story: int | None = None
    score_by_characters: int | None = None
    score_by_drawing: int | None = None
    review: str | None = None
    watch_type: WatchType
