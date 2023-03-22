from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str
    email: EmailStr


class UserID(User):
    id: int


class UserDB(UserID):
    password: str
