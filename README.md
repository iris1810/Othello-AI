# Othello AI

An interactive **Othello (Reversi) game with an AI opponent**, built in **Python and Pygame**. The project implements the complete Othello rule set and uses **Minimax with Alpha-Beta pruning** to make strategic AI decisions.

## Demo

**[Watch the Othello AI Demo on YouTube](https://www.youtube.com/watch?v=EgZoHNykmW4)**

## Features

* **Human vs. Human** and **Human vs. AI** gameplay
* Complete Othello rules with **8-direction move detection and disc flipping**
* Legal-move validation, scoring, pass handling, and game-over detection
* **Minimax AI with Alpha-Beta pruning**
* Adjustable AI search depth
* Weighted evaluation using:

  * Mobility
  * Piece advantage
  * Corner control
* **AI move hints** for the player
* Real-time search diagnostics including **nodes searched, evaluation scores, and pruning behavior**
* Visual indicators for legal moves and game status

## AI Implementation

The AI evaluates possible future board states using the **Minimax algorithm**.

To reduce unnecessary search, **Alpha-Beta pruning** eliminates branches that cannot affect the final decision, allowing the AI to search deeper while evaluating fewer nodes.

The board evaluation function combines:

```text
Board Score =
    Piece Advantage
  + Mobility
  + Corner Control
```

The search depth can be adjusted during gameplay to control the tradeoff between **AI strength and computation time**.

## Screenshots
<img width="1102" height="832" alt="Screenshot 2026-08-25 at 3 15 41 PM" src="https://github.com/user-attachments/assets/bd0e36c8-57ef-49dc-9190-832085f70870" />
<img width="1100" height="826" alt="Screenshot 2026-08-25 at 3 16 19 PM" src="https://github.com/user-attachments/assets/edc0b092-09b2-4a83-9762-d0fe97a5b6b4" />
<img width="1104" height="829" alt="Screenshot 2026-08-25 at 3 16 41 PM" src="https://github.com/user-attachments/assets/57f38c86-e9f4-4970-b99e-aa2965e8408b" />
<img width="780" height="466" alt="Screenshot 2026-08-25 at 3 18 10 PM" src="https://github.com/user-attachments/assets/2a9c9370-1fb1-46a0-9d66-9bb1a0e30296" />
<img width="902" height="731" alt="Screenshot 2026-08-25 at 3 18 41 PM" src="https://github.com/user-attachments/assets/2580b3df-dfa1-4c33-a1d6-ee5680ee86e1" />


## Controls

| Input           | Action                                      |
| --------------- | ------------------------------------------- |
| **Left Click**  | Place a disc on a legal square              |
| **Right Click** | Print board state to console                |
| **1**           | AI plays Black                              |
| **2**           | AI plays White                              |
| **0**           | Disable AI / Human vs. Human                |
| **H**           | Show AI-recommended move                    |
| **A**           | Force AI to make its move                   |
| **M**           | Let AI make one move for the current player |
| **[ / ]**       | Decrease / increase search depth            |
| **P**           | Toggle Alpha-Beta pruning                   |
| **D**           | Toggle Minimax debug output                 |
| **SPACE**       | Reset game                                  |
| **Q**           | Quit                                        |

## Getting Started

### Requirements

* Python 3.8+
* Pygame

Install Pygame:

```bash
pip install pygame
```

Clone the repository:

```bash
git clone https://github.com/iris1810/Othello-AI.git
cd Othello-AI
```

Run the game:

```bash
python3 Othello.py
```

## Tech Stack

**Python • Pygame • Minimax • Alpha-Beta Pruning • Adversarial Search**

## Author

**Khai Tran Nguyen**

CSC 4993 — Artificial Intelligence
Louisiana Tech University
