from datetime import datetime
from typing import List

from pydantic import BaseModel, validator, ValidationError


class GameSchema(BaseModel):
    id: int


class Move(BaseModel):
    id: int
    game_id: int
    board: list
    modified_at: datetime

    class Config:
        from_attributes = True


class GameHistory(BaseModel):
    history: List[Move]


class PlayerMove(BaseModel):
    x: int
    y: int

    @validator("x", "y")
    def check_range(cls, value):
        if not (0 <= value <= 2):
            raise ValueError("You miss the board. Position must be between 0 and 2")
        return value
