from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Form, Request, UploadFile

from database import postgres
from config import API_PREFIX
from schemas import GenreID, PartialAnime, UserID, Anime
from internal.cloud_storage import ImageKitCloudStorage
import dependencies

router = APIRouter(prefix=API_PREFIX)


@router.post("/anime")
async def add_anime(
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    genres: Annotated[str, Form()],
    image_file: UploadFile,
    user: Annotated[UserID, Depends(dependencies.get_current_user)],
    request: Request,
) -> PartialAnime:
    print("add anime", request.cookies)
    # TODO: limit max file size to 1 mb?
    if not user.can_manage_anime():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions to do this action")

    anime_id = await postgres.add_anime(
        name,
        description
    )

    genres_ids = list(map(int, genres.split(",")))
    await postgres.add_anime_genres(anime_id, genres_ids)

    image_url = await ImageKitCloudStorage().upload_file(
        f"/anime/{anime_id}/",
        image_file.file,
        f"{anime_id}"
    )

    await postgres.update_anime(anime_id, image_url=image_url)

    anime_data = await postgres.get_anime(anime_id)
    return PartialAnime(**anime_data)


@router.get("/anime/list")
async def get_anime_list(sort: str | None = None, genres: str | None = None, search: str | None = None):
    genres_ids = list(map(int, genres.split(","))) if genres else None
    return await postgres.get_anime_list(sort, genres_ids, search)


@router.get("/anime/{anime_id}")
async def get_anime(anime_id: int, rating: str | None = None, with_genres: bool = False) -> Anime:
    anime_data = await postgres.get_anime(anime_id)
    if not rating and not with_genres:
        return Anime(**anime_data)

    if rating == "average":
        anime_data["average_rating"] = await postgres.get_average_anime_rating(anime_id)
    elif rating == "total":
        anime_data["total_rating"] = await postgres.get_all_anime_scores(anime_id)
    elif rating == "all":
        anime_data["average_rating"] = await postgres.get_average_anime_rating(anime_id)
        anime_data["total_rating"] = await postgres.get_all_anime_scores(anime_id)

    if with_genres:
        anime_data["genres"] = await postgres.get_anime_genres(anime_id)

    return Anime(**anime_data)



@router.delete("/anime/{anime_id}")
async def delete_anime(anime_id: int, user: Annotated[UserID, Depends(dependencies.get_current_user)]):
    if not user.can_manage_anime():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions to do this action")
    await postgres.delete_anime(anime_id)


@router.get("/genres/list")
async def get_list_genres():
    return await postgres.get_genres()


@router.post("/genres")
async def add_genre(genre_name: str, user: Annotated[UserID, Depends(dependencies.get_current_user)]) -> GenreID:
    if not user.can_manage_anime():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions to do this action")
    genre_id = await postgres.add_genre(genre_name)
    return GenreID(
        name=genre_name,
        id=genre_id
    )


@router.post("/rating")
async def add_anime_rating(
    anime_id: Annotated[int, Form()],
    score: Annotated[int, Form()],
    score_by_story: Annotated[int, Form()],
    score_by_drawing: Annotated[int, Form()],
    score_by_characters: Annotated[int, Form()],
    review: Annotated[str, Form()],
    user: Annotated[UserID, Depends(dependencies.get_current_user)]
):
    await postgres.add_rating(
        anime_id,
        user.id,
        score,
        score_by_story,
        score_by_characters,
        score_by_drawing,
        review
    )
    return {"status": "success"}


@router.get("/rating")
async def get_user_anime_rating(anime_id: int, user: Annotated[UserID, Depends(dependencies.get_current_user)]):
    return await postgres.get_user_anime_rating(anime_id, user.id)
