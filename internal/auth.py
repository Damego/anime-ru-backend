from uuid import uuid4

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_value(value: str) -> str:
    return pwd_context.hash(value)


def verify_hashed_value(value: str, hashed_value: str) -> bool:
    return pwd_context.verify(value, hashed_value)


def create_session_id() -> str:
    return str(uuid4())
