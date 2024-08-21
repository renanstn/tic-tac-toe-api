from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models, schemas
from database import engine, get_db


# Create models if not exist
models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
async def hello():
    return {"Hello": "World"}


@app.post("/game", response_model=schemas.GameSchema)
async def create_game(db: Session = Depends(get_db)):
    game_to_create = models.Game()
    db.add(game_to_create)
    db.commit()
    db.refresh(game_to_create)

    move_to_create = models.Move(game_id=game_to_create.id)
    db.add(move_to_create)
    db.commit()

    return game_to_create

@app.get("/game/{game_id}", response_model=schemas.GameHistory)
async def get_game_history(game_id: int, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        return {"message": f"Game id '{game_id}' not found."}

    moves = db.query(models.Move).filter(models.Move.game_id == game.id).order_by(models.Move.modified_at.asc()).all()
    move_schemas = [schemas.Move.from_orm(move) for move in moves]

    return schemas.GameHistory(history=move_schemas)
