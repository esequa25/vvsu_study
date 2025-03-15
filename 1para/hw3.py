"""
Given a Tic-Tac-Toe 3x3 board (can be unfinished).
Write a function that checks if the are some winners.
If there is "x" winner, function should return "x wins!"
If there is "o" winner, function should return "o wins!"
If there is a draw, function should return "draw!"
If board is unfinished, function should return "unfinished!"

Example:
    [[-, -, o],
     [-, x, o],
     [x, o, x]]
    Return value should be "unfinished"

    [[-, -, o],
     [-, o, o],
     [x, x, x]]

     Return value should be "x wins!"

"""
from typing import List


def tic_tac_toe_checker(board: List[List]) -> str:

    def all_same(line):
        return len(set(line)) == 1 and line[0] != '-'

    # Check rows for a winner
    for row in board:
        if all_same(row):
            return f"{row[0]} wins!"

    # Check columns for a winner
    for col in range(3):
        column = [board[row][col] for row in range(3)]
        if all_same(column):
            return f"{column[0]} wins!"

    # Check diagonals for a winner
    diagonal1 = [board[i][i] for i in range(3)]  # Top-left to bottom-right
    diagonal2 = [board[i][2 - i] for i in range(3)]  # Top-right to bottom-left
    if all_same(diagonal1):
        return f"{diagonal1[0]} wins!"
    if all_same(diagonal2):
        return f"{diagonal2[0]} wins!"

    # Check for draw or unfinished
    for row in board:
        if '-' in row:  # If there's an empty space, the game is unfinished
            return "unfinished!"
    
    # If no winner and no empty spaces, it's a draw
    return "draw!"

check = [["x", "x", "o"],
         ["-", "o", "o"],
         ["o", "-", "x"]]
print(tic_tac_toe_checker(check))
