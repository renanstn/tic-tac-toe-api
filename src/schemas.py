from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, field_validator


class GameSchema(BaseModel):
    id: int
    winner: Optional[str] = None
    modified_at: datetime


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

    @field_validator("x", "y")
    def check_range(cls, value):
        if not (0 <= value <= 2):
            raise ValueError("You miss the board. Position must be between 0 and 2")
        return value
