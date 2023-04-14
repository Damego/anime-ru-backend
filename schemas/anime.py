from pydantic import BaseModel

from .base import IDModel


class Genre(BaseModel):
    name: str


class GenreID(IDModel, Genre):
    ...


class BaseAnime(BaseModel):
    name: str
    image_url: str


class Anime(BaseAnime):
    genres: list[Genre]


class PartialAnime(IDModel, BaseAnime):
    ...
