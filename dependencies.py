from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from internal.oauth2 import decode_access_token
from internal.error import CredentialException
from database import postgres
from schemas import UserDB

oauth2_scheme = OAuth2PasswordBearer("token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserDB:
    data = decode_access_token(token)
    username: str = data.get("sub")

    if username is None:
        raise CredentialException()

    user = await postgres.get_user(username=username)
    if not user:
        raise CredentialException()

    return UserDB(**user)
