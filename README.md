# tic-tac-toe-api

## Time control

> :clock10: Start at: 10:00AM

> Pause between: 12:10PM and 1:00PM

> Finish at: 2:40PM

## Description

TODO

## Setup project

TODO

## Shell commands for tests

### Create game

```sh
curl -X POST http://localhost:8000/game -H "Content-Type: application/json" -d '{}'
```

### Make a move

```sh
curl -X POST "http://localhost:8000/game/5/move" \
     -H "Content-Type: application/json" \
     -d '{"x": 0, "y": 1}'
```

### Show all games

```sh
curl http://localhost:8000/games -H "Content-Type: application/json"
```

### Show moves history from a game

```sh
curl http://localhost:8000/game/4 -H "Content-Type: application/json"
```
