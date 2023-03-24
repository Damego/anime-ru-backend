import asyncpg


class PostgresClient:
    def __init__(self, *, host: str, port: int = 5432, user: str, password: str):
        self._host = host
        self._user = user
        self._port = port
        self._password = password

        self.connection: asyncpg.Connection | None = None  # type: ignore

    async def connect(self):
        self.connection = await asyncpg.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            database="anime",
        )

    async def create_tables(self):
        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS genres (
                genre_id SERIAL,
                genre_name varchar(50) PRIMARY KEY NOT NULL,
            
                UNIQUE (genre_id)
            )"""
        )
        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS anime_titles (
                anime_id SERIAL,
                anime_name varchar(255) PRIMARY KEY NOT NULL,
                description TEXT,
                mal_id integer NOT NULL,
            
                UNIQUE (anime_id)
            )
            """
        )
        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS anime_genres (
                anime_id INTEGER NOT NULL,
                genre_id INTEGER NOT NULL,
                FOREIGN KEY (anime_id) REFERENCES anime_titles(anime_id) ON DELETE CASCADE,
                FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE,
            
                PRIMARY KEY (anime_id, genre_id)
            )
            """
        )
        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id serial,
                user_name varchar(50) NOT NULL,
                user_email varchar(255) PRIMARY KEY NOT NULL,
                user_password varchar(255) NOT NULL,
                permissions integer DEFAULT 0 NOT NULL,

                UNIQUE (user_id),
                UNIQUE (user_name)
            )
            """
        )
        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS watch_types (
                type_id serial,
                type_name varchar(50) PRIMARY KEY NOT NULL,
                
                UNIQUE (type_id)
            )
            """
        )
        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS rating (
                user_id INTEGER NOT NULL,
                anime_id INTEGER NOT NULL,
                score SMALLINT NOT NULL,
                score_by_story SMALLINT,
                score_by_characters SMALLINT,
                score_by_drawing SMALLINT,
                review TEXT,
                watch_type_id INTEGER,
            
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (anime_id) REFERENCES anime_titles(anime_id) ON DELETE CASCADE,
                FOREIGN KEY (watch_type_id) REFERENCES watch_types(type_id) ON DELETE SET NULL,
                PRIMARY KEY (user_id, anime_id)
            )
            """
        )

        await self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                user_id INTEGER,
                session_id varchar(255),

                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                PRIMARY KEY (user_id, session_id)
            )
            """
        )

    async def create_user(
        self,
        name: str,
        email: str,
        password: str
    ):
        await self.connection.execute(
            """
            INSERT INTO users (user_name, user_email, user_password) VALUES ($1, $2, $3)
            """,
            name,
            email,
            password
        )

    async def get_user(self, *, id: int = None, email: str = None, username: str = None) -> dict | None:
        filter = None
        if id is not None:
            filter = "user_id"
        elif email is not None:
            filter = "user_email"
        elif username is not None:
            filter = "user_name"

        record: asyncpg.Record = await self.connection.fetchrow(
            f"""
            SELECT * FROM users WHERE {filter}=$1
            """,
            id or email or username
        )
        if record is None:
            return

        return {
            "id": record[0],
            "name": record[1],
            "email": record[2],
            "password": record[3]
        }

    async def delete_user(self, user_id: int):
        await self.connection.execute(
            """
            DELETE FROM users WHERE user_id=$1
            """,
            user_id
        )

    async def get_user_from_session_id(self, session_id: str) -> dict | None:
        user_id = await self.connection.fetchval("SELECT user_id FROM sessions WHERE session_id=$1", session_id)
        if user_id is None:
            return
        return await self.get_user(id=user_id)

    async def add_session_id(self, user_id: int, session_id: str):
        await self.connection.execute(
            """
            INSERT INTO sessions VALUES ($1, $2)
            """,
            user_id, session_id
        )

    async def get_sessions(self, user_id: int) -> list[str]:
        records = await self.connection.fetch("SELECT session_id FROM sessions WHERE user_id=$1", user_id)
        return [row[0] for row in records]

    # TODO: delete session(s)

    async def add_anime(
        self,
        name: str,
        mal_id: int,
        description: str | None = None
    ) -> int:
        await self.connection.execute(
            """
            INSERT INTO anime_titles (anime_name, description, mal_id) VALUES ($1, $2, $3)
            """,
            name,
            description,
            mal_id
        )
        record = await self.connection.fetchrow("SELECT anime_id FROM anime_titles WHERE anime_name=$1", name)
        return record[0]

    async def get_anime(self, id: int):
        record: asyncpg.Record = await self.connection.fetchrow(
            "SELECT * FROM anime_titles WHERE anime_id=$1", id)
        if record is None:
            return

        genres = await self.connection.fetch(
            """
            SELECT * FROM genres WHERE genres.genre_id IN (SELECT genre_id FROM anime_genres WHERE anime_id=$1)
            """,
            record[0]
        )

        return {
            "id": record[0],
            "name": record[1],
            "description": record[2],
            "mal_id": record[3],
            "genres": [
                {"id": genre[0], "name": genre[1]} for genre in genres
            ]
        }

    async def search_anime(self, name: str):
        record = await self.connection.fetch(
            """SELECT anime_id, anime_name FROM anime_titles WHERE anime_name LIKE $1""", name
        )

        return [
            {"id": anime[0], "name": anime[1]} for anime in record
        ]

    async def delete_anime(self, anime_id: int):
        await self.connection.execute(
            """
            DELETE FROM anime_titles WHERE anime_id=$1
            """,
            anime_id
        )

    async def add_genre(self, name: str) -> int:
        await self.connection.execute(
            "INSERT INTO genres (genre_name) VALUES ($1)", name
        )
        record = await self.connection.fetchrow("SELECT genre_id FROM genres WHERE genre_name=$1", name)
        return record[0]

    async def get_genres(self):
        record = await self.connection.fetch("SELECT * FROM genres")

        return [
            {"id": genre[0], "name": genre[1]} for genre in record
        ]

    async def remove_genre(self, genre_id: int):
        await self.connection.execute(
            """
            DELETE FROM genres WHERE genre_id=$1
            """,
            genre_id
        )

    async def add_anime_genre(self, anime_id: int, genre_id: int):
        await self.connection.execute(
            """
            INSERT INTO anime_genres (anime_id, genre_id) VALUES ($1, $2)
            """,
            anime_id, genre_id
        )

    async def add_anime_genres(self, anime_id: int, genre_ids: list[int]):
        symbol_pairs = []
        args = []
        for i in range(0, len(genre_ids)):
            symbol_pairs.append(f"(${2*i+1}, ${2*i + 2})")
            args.extend((anime_id, genre_ids[i]))

        total = ", ".join(symbol_pairs)

        await self.connection.execute(
            f"""
            INSERT INTO anime_genres (anime_id, genre_id) VALUES {total}
            """,
            *args
        )

    async def remove_anime_genre(self, anime_id: int, genre_id: int):
        await self.connection.execute(
            """
            DELETE FROM anime_genres WHERE anime_id=$1 AND genre_id=$2
            """,
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
        await self.connection.execute(
            """
            INSERT INTO rating (user_id, anime_id, score, score_by_story, score_by_characters, score_by_drawing, review, watch_type_id) VALUES 
            ($1, $2, $3, $4, $5, $6, $7, $8)
            """,
            anime_id, user_id, score, score_by_story, score_by_characters, score_by_drawing, review, watch_type
        )

    async def remove_rating(self, rating_id: int):
        ...
