from fastapi import APIRouter

from database import postgres
from config import API_PREFIX
from schemas import AddAnimePayload, GenreID, AnimeID

router = APIRouter(prefix=API_PREFIX)


@router.post("/animes")
async def add_anime(anime: AddAnimePayload) -> AnimeID:
    anime_id = await postgres.add_anime(
        anime.name,
        anime.mal_id,
        anime.description
    )
    await postgres.add_anime_genres(anime_id, anime.genres)
    anime_data = await postgres.get_anime(anime_id)
    return AnimeID(**anime_data)


@router.get("/animes/{anime_id}")
async def get_anime(anime_id: int) -> AnimeID:
    anime_data = await postgres.get_anime(anime_id)
    return AnimeID(**anime_data)


@router.delete("/animes/{anime_id}")
async def delete_anime(anime_id: int):
    await postgres.delete_anime(anime_id)


@router.post("/animes/genres")
async def add_genre(genre_name: str) -> GenreID:
    genre_id = await postgres.add_genre(genre_name)
    return GenreID(
        name=genre_name,
        id=genre_id
    )
