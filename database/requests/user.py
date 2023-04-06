def add_user() -> str:
    return "INSERT INTO users (user_name, user_email, user_password) VALUES ($1, $2, $3)"


def get_user(*, id: int = None, email: str = None, username: str = None) -> str:
    filter = None
    if id is not None:
        filter = "user_id"
    elif email is not None:
        filter = "user_email"
    elif username is not None:
        filter = "user_name"

    return f"SELECT * FROM users WHERE {filter}=$1"


def delete_user() -> str:
    return "DELETE FROM users WHERE user_id=$1"


def add_session_id() -> str:
    return "INSERT INTO sessions VALUES ($1, $2)"


def get_user_sessions() -> str:
    return "SELECT session_id FROM sessions WHERE user_id=$1"


def get_user_from_session_id() -> str:
    return "SELECT user_id FROM sessions WHERE session_id=$1"


def delete_user_session() -> str:
    return "DELETE FROM sessions WHERE user_id=$1 AND session_id=$2"


def delete_all_user_sessions() -> str:
    return "DELETE FROM sessions WHERE user_id=$1"
