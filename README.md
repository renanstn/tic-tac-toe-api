# tic-tac-toe-api

## Time control

> :clock10: Start at: 10:00AM

> ☕ Pause between: 12:10PM and 1:00PM

> 🕒 Finish at: 3:00PM

## Description

This is the technical test from Ethyca company for Python developer position.

You can find the challenge description [here](https://github.com/ethyca/python-takehome-2).

## How to run

> 🐳 Requires [Docker](https://www.docker.com/products/docker-desktop/) and docker compose

Init database with

```sh
docker compose up -d db
```

Init API with

```sh
docker compose up api
```

API will be available at:

`http://localhost:8000`

## Considerations and issues

- All machine movements are randoms
- Due to restrict challenge time (4 hours), some improvements were left to do, like:
  - Broke the `make_move` handler in small functions
  - More consistent names for schemas
  - Unit tests
  - Reduce repetition
  - A better README
  - Docstrings for all functions

## Shell commands for tests

### Create a new game

```sh
curl -X POST http://localhost:8000/game -H "Content-Type: application/json" -d '{}'
```

### Make a move

```sh
curl -X POST "http://localhost:8000/game/{game_id}/move" \
     -H "Content-Type: application/json" \
     -d '{"x": 0, "y": 1}'
```

### Show all games

```sh
curl http://localhost:8000/games -H "Content-Type: application/json"
```

### Show moves history from a game

```sh
curl http://localhost:8000/game/{game_id} -H "Content-Type: application/json"
```
