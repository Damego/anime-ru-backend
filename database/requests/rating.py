def add_rating():
    return """
        INSERT INTO rating (
            user_id,
            anime_id,
            score,
            score_by_story,
            score_by_characters,
            score_by_drawing,
            review
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7)
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
            count(*) FILTER(WHERE score = 1),
            count(*) FILTER(WHERE score = 2),
            count(*) FILTER(WHERE score = 3),
            count(*) FILTER(WHERE score = 4),
            count(*) FILTER(WHERE score = 5),
            count(*) FILTER(WHERE score = 6),
            count(*) FILTER(WHERE score = 7),
            count(*) FILTER(WHERE score = 8),
            count(*) FILTER(WHERE score = 9),
            count(*) FILTER(WHERE score = 10),
            count(*)
        FROM rating
        WHERE anime_id=$1
    """


def get_average_anime_rating():
    return """
        SELECT
            sum(score) * 1.0 / count(*),
            sum(score_by_story) * 1.0 / count(*),
            sum(score_by_drawing) * 1.0 / count(*),
            sum(score_by_characters) * 1.0 / count(*)
        FROM rating
        WHERE anime_id=$1
    """


def get_user_rating():
    return """
        SELECT * FROM rating WHERE user_id=$1 AND anime_id=$2
    """