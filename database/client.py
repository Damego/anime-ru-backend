import asyncpg

from . import requests


class PostgresClient:
    def __init__(self, *, host: str, port: int = 5432, user: str, password: str):
        self._host = host
        self._user = user
        self._port = port
        self._password = password

        self.connection_pool: asyncpg.Pool | None = None

    async def connect(self):
        self.connection_pool = await asyncpg.create_pool(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            database="anime",
        )

    async def create_tables(self):
        await self.connection_pool.execute(requests.create_genres_table())
        await self.connection_pool.execute(requests.create_anime_titles_table())
        await self.connection_pool.execute(requests.create_anime_genres_table())
        await self.connection_pool.execute(requests.create_users_table())
        await self.connection_pool.execute(requests.create_watch_types_table())
        await self.connection_pool.execute(requests.create_rating_table())
        await self.connection_pool.execute(requests.create_sessions_table())

    async def create_user(
        self,
        name: str,
        email: str,
        password: str
    ):
        await self.connection_pool.execute(
            requests.add_user(),
            name,
            email,
            password
        )

    async def get_user(self, *, id: int = None, email: str = None, username: str = None) -> dict | None:
        record: asyncpg.Record = await self.connection_pool.fetchrow(
            requests.get_user(id=id, email=email, username=username),
            id or email or username
        )
        if record is None:
            return

        return {
            "id": record[0],
            "name": record[1],
            "email": record[2],
            "password": record[3],
            "permissions": record[4]
        }

    async def delete_user(self, user_id: int):
        await self.connection_pool.execute(
            requests.delete_user(),
            user_id
        )

    async def get_user_from_session_id(self, session_id: str) -> dict | None:
        user_id = await self.connection_pool.fetchval(requests.get_user_from_session_id(), session_id)
        if user_id is None:
            return
        return await self.get_user(id=user_id)

    async def add_session_id(self, user_id: int, session_id: str):
        await self.connection_pool.execute(
            requests.add_session_id(),
            user_id, session_id
        )

    async def get_sessions(self, user_id: int) -> list[str]:
        records = await self.connection_pool.fetch(requests.get_user_sessions(), user_id)
        return [row[0] for row in records]

    # TODO: delete session(s)

    async def add_anime(
        self,
        name: str,
        description: str | None = None
    ) -> int:
        await self.connection_pool.execute(
            requests.add_anime(),
            name,
            description,
        )
        # It's maybe the worst way to get ID from the inserted string
        return await self.connection_pool.fetchval(requests.get_anime_id_by_name(), name)

    async def update_anime(
        self,
        id: int,
        name: str | None = None,
        description: str | None = None,
        image_url: str | None = None,
    ):
        request_string, args = requests.update_anime(id, name, description, image_url)

        await self.connection_pool.execute(
            request_string,
            *args
        )

    async def get_anime(self, id: int):
        record: asyncpg.Record = await self.connection_pool.fetchrow(
            requests.get_anime_data(), id)
        if record is None:
            return

        return {
            "id": record[0],
            "name": record[1],
            "description": record[2],
            "image_url": record[3],
        }

    async def get_anime_list(self, sort: str | None = None, genres: list[int] | None = None, search: str | None = False):
        has_search = search is not None
        args = [f"%{search}%"] if has_search else []

        if sort is not None and genres is not None:
            record = await self.connection_pool.fetch(
                requests.get_sorted_filtered_anime_list(sort, genres, has_search), *args
            )
        elif sort is not None:
            record = await self.connection_pool.fetch(requests.get_sorted_anime_list(sort, has_search), *args)
        elif genres is not None:
            record = await self.connection_pool.fetch(requests.get_filtered_anime_list(genres, has_search), *args)
        else:
            record = await self.connection_pool.fetch(requests.get_anime_list(has_search), *args)

        if record is None:
            return

        data = []
        for anime_ in record:
            data.append({
                "id": anime_[0],
                "name": anime_[1],
                "image_url": anime_[2],
                "average_rating": anime_[3]
            })

        return data

    async def get_all_anime_scores(self, anime_id: int):
        record = await self.connection_pool.fetchrow(requests.get_anime_scores(), anime_id)
        if not any(record):
            return
        data = {
            f"score_{i + 1}": record[i]
            for i in range(10)
        }
        data["total"] = record[10]
        return data


    async def get_average_anime_rating(self, anime_id: int):
        record = await self.connection_pool.fetchrow(requests.get_average_anime_rating(), anime_id)
        if not any(record):
            return

        return {
            "score": record[0],
            "score_by_story": record[1],
            "score_by_drawing": record[2],
            "score_by_characters": record[3],
        }

    async def get_anime_genres(self, anime_id: int):
        record = await self.connection_pool.fetch(requests.get_anime_genres(), anime_id)

        return [
            {"id": genre[0], "name": genre[1]} for genre in record
        ]

    async def search_anime(self, name: str):
        record = await self.connection_pool.fetch(
            requests.search_anime(), f"%{name}%"
        )

        return [
            {"id": anime[0], "name": anime[1]} for anime in record
        ]

    async def delete_anime(self, anime_id: int):
        await self.connection_pool.execute(
            requests.delete_anime_by_id(),
            anime_id
        )

    async def add_genre(self, name: str) -> int:
        await self.connection_pool.execute(
            requests.add_genre(), name
        )
        return await self.connection_pool.fetchval(requests.get_genre_id_by_name(), name)

    async def get_genres(self):
        record = await self.connection_pool.fetch(requests.get_all_genres())

        return [
            {"id": genre[0], "name": genre[1]} for genre in record
        ]

    async def remove_genre(self, genre_id: int):
        await self.connection_pool.execute(
            requests.delete_genre_by_id(),
            genre_id
        )

    async def add_anime_genre(self, anime_id: int, genre_id: int):
        await self.connection_pool.execute(
            requests.add_anime_genre(),
            anime_id, genre_id
        )

    async def add_anime_genres(self, anime_id: int, genre_ids: list[int]):
        request_string, args = requests.add_anime_genres(anime_id, genre_ids)

        await self.connection_pool.execute(
            request_string,
            *args
        )

    async def remove_anime_genre(self, anime_id: int, genre_id: int):
        await self.connection_pool.execute(
            requests.delete_anime_genre(),
            anime_id, genre_id
        )

    async def add_rating(
        self,
        anime_id: int,
        user_id: int,
        score: int,
        score_by_story: int | None = None,
        score_by_characters: int | None = None,
        score_by_drawing: int | None = None,
        review: str | None = None,
        watch_type: int | None = None
     ):
        await self.connection_pool.execute(
            requests.add_rating(),
            anime_id, user_id, score, score_by_story, score_by_characters, score_by_drawing, review, watch_type
        )

    async def remove_rating(self, rating_id: int):
        ...
