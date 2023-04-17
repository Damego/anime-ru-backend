from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

load_dotenv() # noqa
from database import postgres
from routes import anime, users


app = FastAPI()
app.include_router(anime.router)
app.include_router(users.router)


@app.on_event("startup")
async def start():
    await postgres.connect()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "anime-ru.vercel.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Set-Cookie"],
)