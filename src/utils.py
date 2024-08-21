def check_victory(table: list, player: str) -> bool:
    """
    Check victory conditions for a player.
    """
    # Check horizontals
    for line in table:
        if line == [player, player, player]:
            return True
    # Check verticals
    for column in range(3):
        if all(table[row][column] == player for row in range(3)):
            return True
    # Check diagonals
    if table[0][0] == table[1][1] == table[2][2] == player:
        return True
    if table[0][2] == table[1][1] == table[2][0] == player:
        return True

    return False
