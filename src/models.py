from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func

from database import Base


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, index=True)
    finished = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
