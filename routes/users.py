from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Form, Response, Cookie

import dependencies
from internal import auth, error
from schemas import UserDB
from database import postgres
from config import API_PREFIX


router = APIRouter(prefix=API_PREFIX)


async def auth_user(username: str, password: str):
    user_data = await postgres.get_user(username=username)
    if not user_data:
        return

    user = UserDB(**user_data)

    if not auth.verify_hashed_value(password, user.password):
        return

    return user


@router.post("/auth")
async def authorize_user(
    login: Annotated[str, Form()],
    password: Annotated[str, Form()],
    response: Response
):
    user = await auth_user(login, password)

    if user is None:
        raise error.InvalidUserData()

    session_id = auth.create_session_id()

    await postgres.add_session_id(
        user.id, session_id
    )

    response.set_cookie("session_id", session_id)

    return {
        "session_id": session_id
    }


@router.get("/users/me")
async def get_current_user(session_id: Annotated[str, Cookie()]):
    return await dependencies.get_current_user(session_id)


@router.post("/users")
async def register(username: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()]):
    user = await postgres.get_user(username=username) or await postgres.get_user(email=email)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    hashed_password = auth.hash_value(password)
    await postgres.create_user(username, email, hashed_password)

    return {
        "status": "success"
    }

