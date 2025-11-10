Author: Khai Tran Nguyen
Course: CSC 4993 – Artificial Intelligence
Date: Nov 2025

Othello Game (with Optional AI)

I. Overview

This program implements the full rules of the classic Othello (Reversi) board game using Python + Pygame.
It allows:
    - Two human players to play against each other (default mode)
    - Or a Human vs Computer (AI) mode, using a Minimax search with optional Alpha-Beta pruning.

All legal move generation, disc flipping, pass handling, and game-over detection follow official Othello rules.

II. Requirements
    - Python ≥ 3.8
    - The image files for tokens should exist inside a tokens/ folder in the same directory

III. Game Control
In your terminal: let run python3 Othello.py (macbook)
You will see:
    Welcome to Othello!
    You can play:
    - Human vs Human (default)
    - Human vs AI (press 1 or 2 to choose AI color)
    - Press 0 to disable AI (return to 2-player mode)
    - Press SPACE to reset, Q to quit

This is for the controls:
    Key        |      Mouse Action
    Left Click	 Place a disc at the selected square (if legal).
    Right Click  Print the current logic board to console (for debugging).
    Q	         Quit the game.
    SPACE        Reset the game to the starting 4 discs.
    1 -  Set AI = Black (AI moves first).
    2 - Set AI = White (Human moves first).
    0 - Disable AI → 2-Player Mode.
    A - Force the AI to make its move immediately (when it’s its turn).
    H - Show a hint: best move for the current player.
    M - Let the computer play one move for the current player.
    [ / ]	Decrease / increase AI search depth.
    P	Toggle Alpha-Beta pruning ON/OFF.
    D	Toggle debug mode (prints Minimax exploration tree).

IV. Implement AI
Algorithm: Minimax with optional Alpha-Beta pruning

Evaluation Function: Weighted heuristic combining
    Piece difference
    Mobility (number of available moves)
    Corner occupancy bonus

Search Depth: Adjustable (default = 3)

Debug Mode: Prints recursion trace, node counts, and pruning info.

V. Game Features
This AI Othello have Full Othello rule implementation, it allow us have move detection in all 8 directions. During the game, it can flip of outflanked discs. It is also contain the skips rule for player if they has no legal moves. The game ends when neither player can move or board is full. Moreove, it has an accurate scoring and winner detection. The option for play game is 2-Player & AI Modes toggleable anytime. Enven better with a visual hints for valid moves. Everything is coming with the display, it include the displays scores, AI depth, pruning status, nodes searched, evaluation value, and current mode.



