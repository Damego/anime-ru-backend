from typing import Annotated

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

load_dotenv()

from schemas import User, UserDB
from database import postgres
from routes import anime



app = FastAPI()

app.include_router(anime.router)

oauth2scheme = OAuth2PasswordBearer("token")


@app.on_event("startup")
async def start():
    await postgres.connect()


async def fake_decode_token(token):
    user = await postgres.get_user(username=token)
    if not user:
        return
    return UserDB(**user)


async def _get_current_user(token: Annotated[str, Depends(oauth2scheme)]):
    user = await fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_data = await postgres.get_user(username=form_data.username)
    if not user_data:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    user = UserDB(**user_data)

    if user.password != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": user.name, "token_type": "bearer"
    }


@app.get("/users/me")
async def get_current_user(user: Annotated[User, Depends(_get_current_user)]):
    return user
