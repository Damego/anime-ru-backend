from pydantic import BaseModel

from .base import IDModel


class Genre(BaseModel):
    name: str


class GenreID(IDModel, Genre):
    ...


class BaseAnime(BaseModel):
    name: str
    image_url: str


class PartialAnime(IDModel, BaseAnime):
    ...


class AverageRating(BaseModel):
    score: float
    score_by_story: float
    score_by_drawing: float
    score_by_characters: float


class TotalRating(BaseModel):
    score_1: float
    score_2: float
    score_3: float
    score_4: float
    score_5: float
    score_6: float
    score_7: float
    score_8: float
    score_9: float
    score_10: float
    total: float


class Anime(PartialAnime):
    description: str
    average_rating: AverageRating | None = None
    total_rating: TotalRating | None = None
    genres: list[GenreID] | None = None
