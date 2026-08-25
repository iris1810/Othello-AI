# Othello AI

An interactive **Othello (Reversi) game with an AI opponent**, built in **Python and Pygame**. The project implements the complete Othello rule set and uses **Minimax with Alpha-Beta pruning** to make strategic AI decisions.

## Demo

**[Watch the Othello AI Demo on YouTube](https://www.youtube.com/watch?v=K9rsMnxV6FA)**

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
<img width="1150" height="463" alt="Screenshot 2026-08-25 at 3 06 04 PM" src="https://github.com/user-attachments/assets/5e262dca-46b9-4616-8786-9c3ef85762f5" />
<img width="1155" height="471" alt="Screenshot 2026-08-25 at 3 06 30 PM" src="https://github.com/user-attachments/assets/f88982ab-e688-4b37-a91c-4c87be5029e4" />
<img width="1333" height="872" alt="Screenshot 2026-08-25 at 3 06 54 PM" src="https://github.com/user-attachments/assets/1a9fcf25-ec9e-4a05-a651-92d53a730f23" />
<img width="845" height="459" alt="Screenshot 2026-08-25 at 3 07 23 PM" src="https://github.com/user-attachments/assets/84a49bb1-bcf0-4c8e-8572-b846f305be7f" />

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
