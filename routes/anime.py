from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from database import postgres
from config import API_PREFIX
from schemas import AddAnimePayload, GenreID, AnimeID, UserID
import dependencies

router = APIRouter(prefix=API_PREFIX)


@router.post("/animes")
async def add_anime(anime: AddAnimePayload, user: Annotated[UserID, Depends(dependencies.get_current_user)]) -> AnimeID:
    if not user.can_manage_anime():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions to do this action")

    anime_id = await postgres.add_anime(
        anime.name,
        anime.mal_id,
        anime.description
    )
    await postgres.add_anime_genres(anime_id, anime.genres)
    anime_data = await postgres.get_anime(anime_id)
    return AnimeID(**anime_data)


@router.get("/animes")
async def get_all_anime_titles():
    return await postgres.get_all_anime()


@router.get("/animes/{anime_id}")
async def get_anime(anime_id: int) -> AnimeID:
    anime_data = await postgres.get_anime(anime_id)
    return AnimeID(**anime_data)


@router.delete("/animes/{anime_id}")
async def delete_anime(anime_id: int, user: Annotated[UserID, Depends(dependencies.get_current_user)]):
    if not user.can_manage_anime():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions to do this action")
    await postgres.delete_anime(anime_id)


@router.post("/animes/genres")
async def add_genre(genre_name: str, user: Annotated[UserID, Depends(dependencies.get_current_user)]) -> GenreID:
    if not user.can_manage_anime():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions to do this action")
    genre_id = await postgres.add_genre(genre_name)
    return GenreID(
        name=genre_name,
        id=genre_id
    )
