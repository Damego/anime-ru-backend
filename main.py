from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv() # noqa
from database import postgres
from routes import anime, users


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(anime.router)
app.include_router(users.router)


@app.on_event("startup")
async def start():
    await postgres.connect()


@app.get("/")
async def index():
    return {
        "test": "yes"
    }