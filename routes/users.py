from fastapi import APIRouter

from config import API_PREFIX
from schemas import UserDB

router = APIRouter(prefix=API_PREFIX)


@router.post("/users")
async def add_user(user: UserDB):
    ...


