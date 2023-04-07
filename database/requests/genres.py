def get_anime_genres():
    return """
    SELECT
        genre_id,
        (SELECT genre_name FROM genres WHERE genres.genre_id=anime_genres.genre_id)
    FROM anime_genres WHERE anime_id=$1;
"""


def add_genre() -> str:
    return "INSERT INTO genres (genre_name) VALUES ($1)"


def get_genre_id_by_name() -> str:
    return "SELECT genre_id FROM genres WHERE genre_name=$1"


def get_all_genres() -> str:
    return "SELECT * FROM genres"


def delete_genre_by_id() -> str:
    return "DELETE FROM genres WHERE genre_id=$1"