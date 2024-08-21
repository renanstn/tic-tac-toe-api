from pydantic import BaseModel


class GameSchema(BaseModel):
    id: int
