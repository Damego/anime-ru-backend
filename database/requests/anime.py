def get_sort_by_type(sort_type: str) -> str:
    match sort_type:
        case "a":
            return "ORDER BY anime_name"
        case "r":
            return "ORDER BY average_score DESC NULLS LAST"
        case "p":
            return "ORDER BY (SELECT count(*) FROM rating WHERE rating.anime_id = anime_titles.anime_id) DESC NULLS LAST"


def get_sorted_anime_list(sort_type: str) -> str:
    return f"""
    SELECT
        anime_id,
        anime_name,
        image_url,
        (SELECT (sum(score) * 1.0 / count(*)) FROM rating WHERE rating.anime_id = anime_titles.anime_id) AS average_score
    FROM anime_titles
    {get_sort_by_type(sort_type)}
    """


def get_filtered_anime_list(genres: list[int]) -> str:
    return f"""
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


def get_sorted_filtered_anime_list(sort_type: str, genres: list[int]) -> str:
    return f"""
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
    {get_sort_by_type(sort_type)}
    """


def get_anime_list() -> str:
    return "SELECT * FROM anime_titles"


def add_anime() -> str:
    return "INSERT INTO anime_titles (anime_name, description) VALUES ($1, $2)"


def get_anime_id_by_name() -> str:
    return "SELECT anime_id FROM anime_titles WHERE anime_name=$1"


def update_anime(
    id: int,
    name: str | None = None,
    description: str | None = None,
    image_url: str | None = None,
) -> tuple[str, list[str]]:
    args = []
    strings = []
    count = 0

    # I don't think this is good but idk
    if name is not None:
        count += 1
        strings.append(f"anime_name=${count}")
        args.append(name)
    if description is not None:
        count += 1
        strings.append(f"anime_description=${count}")
        args.append(description)
    if image_url is not None:
        count += 1
        strings.append(f"image_url=${count}")
        args.append(image_url)

    return f"UPDATE anime_titles SET {', '.join(strings)} WHERE anime_id={id}", args


def get_anime_data() -> str:
    return "SELECT * FROM anime_titles WHERE anime_id=$1"


def search_anime() -> str:
    return "SELECT anime_id, anime_name FROM anime_titles WHERE anime_name LIKE $1"


def delete_anime_by_id() -> str:
    return "DELETE FROM anime_titles WHERE anime_id=$1"
