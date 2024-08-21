from datetime import datetime
from typing import List

from pydantic import BaseModel


class GameSchema(BaseModel):
    id: int


class Move(BaseModel):
    id: int
    game_id: int
    board: list
    modified_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class GameHistory(BaseModel):
    history: List[Move]
