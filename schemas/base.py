from pydantic import BaseModel


class IDModel(BaseModel):
    id: int
