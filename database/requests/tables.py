def create_genres_table() -> str:
    return """
        CREATE TABLE IF NOT EXISTS genres (
            genre_id SERIAL,
            genre_name varchar(20) PRIMARY KEY NOT NULL,
        
            UNIQUE (genre_id)
        )
    """


def create_anime_titles_table() -> str:
    return """
        CREATE TABLE IF NOT EXISTS anime_titles (
            anime_id SERIAL,
            anime_name varchar(100) PRIMARY KEY NOT NULL,
            description TEXT,
            image_url varchar(120),
            start_date DATE,
            end_date DATE,
            
            UNIQUE (anime_id)
        )
    """


def create_anime_genres_table() -> str:
    return """
        CREATE TABLE IF NOT EXISTS anime_genres (
            anime_id INTEGER NOT NULL,
            genre_id INTEGER NOT NULL,
        
            FOREIGN KEY (anime_id) REFERENCES anime_titles(anime_id) ON DELETE CASCADE,
            FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE,
        
            PRIMARY KEY (anime_id, genre_id)
        )
    """


def create_users_table() -> str:
    return """
        CREATE TABLE IF NOT EXISTS users (
            user_id serial,
            user_name varchar(32) NOT NULL,
            user_email varchar(64) PRIMARY KEY NOT NULL,
            user_password varchar(32) NOT NULL,
            permissions integer DEFAULT 0 NOT NULL,
        
            UNIQUE (user_id),
            UNIQUE (user_name)
        )
    """


def create_watch_types_table() -> str:
    return """
        CREATE TABLE IF NOT EXISTS watch_types (
            type_id serial,
            type_name varchar(15) PRIMARY KEY NOT NULL,
        
            UNIQUE (type_id)
        )
    """


def create_rating_table() -> str:
    return """
        CREATE TABLE IF NOT EXISTS rating (
            user_id INTEGER NOT NULL,
            anime_id INTEGER NOT NULL,
            score SMALLINT NOT NULL CHECK (score >= 1 AND score <= 10),
            score_by_story SMALLINT CHECK (score_by_story >= 1 AND score_by_story <= 10),
            score_by_characters SMALLINT CHECK (score_by_characters >= 1 AND score_by_characters <= 10),
            score_by_drawing SMALLINT CHECK (score_by_drawing >= 1 AND score_by_drawing <= 10),
            review TEXT,
            watch_type_id INTEGER,
        
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (anime_id) REFERENCES anime_titles(anime_id) ON DELETE CASCADE,
            FOREIGN KEY (watch_type_id) REFERENCES watch_types(type_id) ON DELETE SET NULL,
            PRIMARY KEY (user_id, anime_id)
        )
    """


def create_sessions_table() -> str:
    return """
        CREATE TABLE IF NOT EXISTS sessions (
            user_id INTEGER,
            session_id varchar(255),
    
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            PRIMARY KEY (user_id, session_id)
        )
    """