import random
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session


import models, schemas
from database import engine, get_db
from utils import check_victory, check_if_board_is_full


# Create database models if not exist
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


@app.get("/games", response_model=List[schemas.GameSchema])
async def get_all_games(db: Session = Depends(get_db)):
    games = db.query(models.Game).order_by(models.Game.modified_at.asc()).all()
    return games


@app.get("/game/{game_id}", response_model=schemas.GameHistory)
async def get_game_history(game_id: int, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail=f"Game id '{game_id}' not found.")
    moves = (
        db.query(models.Move)
        .filter(models.Move.game_id == game.id)
        .order_by(models.Move.modified_at.asc())
        .all()
    )
    move_schemas = [schemas.Move.from_orm(move) for move in moves]
    return schemas.GameHistory(history=move_schemas)


@app.post("/game/{game_id}/move")
async def make_move(
    game_id: int, move: schemas.PlayerMove, db: Session = Depends(get_db)
):
    """
    - Receive the payload
    - Check if values is between 0 and 2
    - Check if position is already played
    - Save move
    - Check victory
    - Make machine move
    - Check victory
    - Return board
    """
    # Check if the game exists and is not finished
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail=f"Game id '{game_id}' not found.")
    if game.winner:
        raise HTTPException(
            status_code=404, detail=f"Game already over. Winner was '{game.winner}'"
        )

    # Get this game last move
    last_move = (
        db.query(models.Move)
        .filter(models.Move.game_id == game.id)
        .order_by(models.Move.modified_at.desc())
        .first()
    )

    # Check if player's position is empty
    if last_move.board[move.x][move.y] != ".":
        raise HTTPException(status_code=404, detail="Position already played")

    # Save player movement
    board_for_player_move = last_move.board
    board_for_player_move[move.x][move.y] = "X"
    player_move = models.Move(game_id=game.id, board=board_for_player_move)
    db.add(player_move)
    db.commit()
    db.refresh(player_move)

    # Check player victory
    if check_victory(player_move.board, "X"):
        game.winner = "player"
        db.commit()
        return {"message": "Congratulations, you win!"}

    # Check game draw
    if check_if_board_is_full(player_move.board):
        game.winner = "draw"
        db.commit()
        return {"message": "Draw game!"}

    # Machine movement
    board_for_machine_move = player_move.board
    # Find free positions on board
    free_positions = [
        (i, j)
        for i in range(3)
        for j in range(3)
        if board_for_machine_move[i][j] == "."
    ]
    if not free_positions:
        game.winner = "draw"
        db.commit()
        return {"message": "Draw game!"}
    # Randomize machine play
    i, j = random.choice(free_positions)
    board_for_machine_move[i][j] = "O"

    # Save machine movement
    machine_move = models.Move(game_id=game.id, board=board_for_machine_move)
    db.add(machine_move)
    db.commit()
    db.refresh(machine_move)

    # Check machine victory
    if check_victory(machine_move.board, "O"):
        game.winner = "machine"
        db.commit()
        return {"message": "You loose!"}

    return {"board": machine_move.board}
