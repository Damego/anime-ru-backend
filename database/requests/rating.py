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