from typing import Annotated

from dotenv import load_dotenv
load_dotenv() # noqa
from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm

import dependencies
from internal import oauth2, error
from schemas import User, UserDB
from database import postgres
from routes import anime


app = FastAPI()

app.include_router(anime.router)


@app.on_event("startup")
async def start():
    await postgres.connect()


async def auth_user(username: str, password: str):
    user_data = await postgres.get_user(username=username)
    if not user_data:
        return

    user = UserDB(**user_data)

    if not oauth2.verify_password(password, user.password):
        return

    return user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await auth_user(form_data.username, form_data.password)

    if user is None:
        raise error.InvalidUserData()

    access_token = oauth2.create_access_token({"sub": form_data.username})

    return {
        "access_token": access_token, "token_type": "bearer"
    }


@app.get("/users/me")
async def get_current_user(user: Annotated[User, Depends(dependencies.get_current_user)]):
    return user


@app.post("/users")
async def register(username: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()]):
    user = await postgres.get_user(username=username) or await postgres.get_user(email=email)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    hashed_password = oauth2.get_password_hash(password)
    await postgres.create_user(username, email, hashed_password)

    return {
        "status": "success"
    }
