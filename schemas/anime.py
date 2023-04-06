from pydantic import BaseModel

from .base import IDModel


class Genre(BaseModel):
    name: str


class GenreID(IDModel, Genre):
    ...


class BaseAnime(BaseModel):
    name: str
    description: str | None = None
    mal_id: int


class Anime(BaseAnime):
    genres: list[Genre]


class AnimeID(IDModel, BaseAnime):
    genres: list[GenreID]
