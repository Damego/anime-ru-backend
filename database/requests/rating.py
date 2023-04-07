def add_rating():
    return """
        INSERT INTO rating (
            user_id,
            anime_id,
            score,
            score_by_story,
            score_by_characters,
            score_by_drawing,
            review,
            watch_type_id
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
    """


def get_anime_watch_type_count() -> str:
    return """
    SELECT
        count(*) FILTER(WHERE watch_type_id = 1),
        count(*) FILTER(WHERE watch_type_id = 2),
        count(*) FILTER(WHERE watch_type_id = 3),
        count(*) FILTER(WHERE watch_type_id = 4),
        count(*) FILTER(WHERE watch_type_id = 5)
    FROM rating
    WHERE anime_id=$1
    """


def get_anime_scores():
    return """
        SELECT 
            count(*) FILTER(WHERE score = 1) as "Оценка 1",
            count(*) FILTER(WHERE score = 2) as "Оценка 2",
            count(*) FILTER(WHERE score = 3) as "Оценка 3",
            count(*) FILTER(WHERE score = 4) as "Оценка 4",
            count(*) FILTER(WHERE score = 5) as "Оценка 5",
            count(*) FILTER(WHERE score = 6) as "Оценка 6",
            count(*) FILTER(WHERE score = 7) as "Оценка 7",
            count(*) FILTER(WHERE score = 8) as "Оценка 8",
            count(*) FILTER(WHERE score = 9) as "Оценка 9",
            count(*) FILTER(WHERE score = 10) as "Оценка 10"
        FROM rating
        WHERE anime_id=$1
    """