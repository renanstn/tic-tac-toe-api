from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB


from database import Base


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, index=True)
    winner = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    modified_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    moves = relationship("Move", back_populates="game")


class Move(Base):
    __tablename__ = "move"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("game.id"))
    board = Column(
        JSONB,
        default=[
            [".", ".", "."],
            [".", ".", "."],
            [".", ".", "."],
        ],
    )
    modified_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    game = relationship("Game", back_populates="moves")
