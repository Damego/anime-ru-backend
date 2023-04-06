def add_anime_genre() -> str:
    return "INSERT INTO anime_genres (anime_id, genre_id) VALUES ($1, $2)"


def add_anime_genres(anime_id: int, genre_ids: list[int]) -> tuple[str, list[int]]:
    symbol_pairs = []
    args = []
    for i in range(0, len(genre_ids)):
        symbol_pairs.append(f"(${2 * i + 1}, ${2 * i + 2})")
        args.extend((anime_id, genre_ids[i]))

    total = ", ".join(symbol_pairs)

    return f"INSERT INTO anime_genres (anime_id, genre_id) VALUES {total}", args


def delete_anime_genre():
    return "DELETE FROM anime_genres WHERE anime_id=$1 AND genre_id=$2"