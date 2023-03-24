from pydantic import BaseModel, EmailStr

from internal.flags import Permissions


class User(BaseModel):
    name: str
    email: EmailStr
    permissions: Permissions

    def has_permissions(self, permissions: Permissions) -> bool:
        return permissions in self.permissions

    def can_manage_anime(self) -> bool:
        return self.has_permissions(Permissions.MANAGE_ANIME_TITLES)

    def can_manage_ratings(self) -> bool:
        return self.has_permissions(Permissions.MANAGE_RATINGS)


class UserID(User):
    id: int


class UserDB(UserID):
    password: str
