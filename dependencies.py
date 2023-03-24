from typing import Annotated

from fastapi import Depends, Cookie
from internal.error import SessionIDExpired
from database import postgres
from schemas import UserID


async def get_current_user(session_id: Annotated[str, Cookie()]) -> UserID:
    user = await postgres.get_user_from_session_id(session_id)
    if not user:
        raise SessionIDExpired()

    return UserID(**user)

