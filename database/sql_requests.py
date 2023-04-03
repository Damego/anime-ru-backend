import asyncpg


class SQLRequests:
    connection: asyncpg.Connection

    async def get_anime_list(self):
        return await self.connection.fetch(
            "SELECT * FROM anime_titles"
        )

    @staticmethod
    def _get_sort_by_type(sort_type: str) -> str:
        match sort_type:
            case "a":
                return "\nORDER BY anime_name"
            case "r":
                return "\nORDER BY average_score DESC NULLS LAST;"
            case "p":
                return "\nORDER BY (SELECT count(*) FROM rating WHERE rating.anime_id = anime_titles.anime_id) DESC NULLS LAST;"


    async def get_sorted_anime_list(self, sort_type: str) -> list[asyncpg.Record]:
        request_string = """
        SELECT
            anime_id,
            anime_name,
            image_url,
            (SELECT (sum(score) * 1.0 / count(*)) FROM rating WHERE rating.anime_id = anime_titles.anime_id) AS average_score
        FROM anime_titles
        """
        request_string += self._get_sort_by_type(sort_type)
        return await self.connection.fetch(request_string)

    async def get_filtered_anime_list(self, genres: list[int]):
        request_string = f"""
        SELECT
            anime_id,
            anime_name,
            image_url
        FROM anime_titles
        WHERE exists (
            SELECT DISTINCT
                anime_id
            FROM anime_genres
            WHERE anime_genres.anime_id=anime_titles.anime_id AND genre_id IN ({', '.join(map(str, genres))})
            )
        """
        return await self.connection.fetch(request_string)

    async def get_sorted_filtered_anime_list(self, sort_type: str, genres: list[int]):
        request_string = f"""
        SELECT
            anime_id,
            anime_name,
            image_url,
            (SELECT (sum(score) * 1.0 / count(*)) FROM rating WHERE rating.anime_id = anime_titles.anime_id) AS average_score
        FROM anime_titles
        WHERE exists (
            SELECT DISTINCT
                anime_id
            FROM anime_genres
            WHERE anime_genres.anime_id=anime_titles.anime_id AND genre_id IN ({', '.join(map(str, genres))})
            )
        ORDER BY average_score DESC NULLS LAST
        """
        request_string += self._get_sort_by_type(sort_type)

        return await self.connection.fetch(request_string)