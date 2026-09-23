# chessBotCreator

A playable chess game with a custom-built AI opponent, written in Python. You play as White against a bot that searches ahead with **minimax, alpha-beta pruning and quiescence search**, and evaluates positions using hand-tuned piece values and piece-square tables.

<!-- Add a screenshot or GIF here, e.g. ![Gameplay](assets/screenshot.png) -->

## Features

- **Play against the bot** in a Pygame window: click a piece, then click a destination square
- **Chess AI** built from scratch on top of `python-chess` for move generation and rules
- **Full rules support**: legal-move validation, check, checkmate, stalemate, and pawn promotion (choose Queen, Rook, Bishop or Knight)
- **Live game panel**: whose turn it is, check / checkmate / stalemate alerts, and a scrollable move history in standard algebraic notation (SAN)
- **Selected-square highlighting** for easier play

## How the bot works

The engine lives in `chessGame.py` and combines several classic techniques:

| Technique | What it does |
|---|---|
| **Minimax with alpha-beta pruning** | Searches the game tree to a fixed depth (default: 3 plies) and skips branches that can't affect the result |
| **Quiescence search** | At the search horizon, keeps resolving captures so the bot doesn't misjudge positions mid-exchange |
| **Move ordering** | Tries the most promising captures first (high-value victim, low-value attacker), which makes pruning far more effective |
| **Transposition table** | Caches evaluated positions using Zobrist hashes (`chess.polyglot`) to avoid re-searching the same position |
| **Static evaluation** | Material values plus piece-square tables for pawns, knights, bishops, rooks and queens, with bonuses for central pawns and developed minor pieces |
| **Repetition handling** | Scores threefold repetition as a draw and penalises twofold repetition so the bot avoids shuffling |

## Getting started

### Requirements

- Python 3.8+
- [pygame](https://www.pygame.org/)
- [chess](https://pypi.org/project/chess/) (python-chess)

### Install and run

```bash
git clone https://github.com/ronakVisram2006/chessBotCreator-private.git
cd chessBotCreator-private

pip install pygame chess

python chessGame.py
```

## How to play

1. You are **White** and move first.
2. Click one of your pieces to select it, then click the square you want to move to.
3. If a pawn reaches the last rank, a promotion menu appears on the left. Click the piece you want.
4. The bot replies as **Black** automatically.
5. Use the **mouse wheel** over the window to scroll the move history.

## Project structure

```
chessBotCreator/
├── chessGame.py   # Game loop, UI, evaluation and search
├── assets/        # Chess piece images
└── README.md
```

## Configuration

To make the bot stronger or faster, change the search depth in `main()`:

```python
move = get_best_move(board, depth=3)
```

Higher depths play better but take noticeably longer per move in Python.

## Possible improvements (will implement soon)

- Let the player choose their colour
- Add a difficulty selector (search depth) in the UI
- Iterative deepening with a time limit per move
- Store bound types (exact / lower / upper) in the transposition table for more accurate cached scores
- Show piece icons in the promotion menu instead of text labels
- Add a king safety and endgame evaluation

## Built with

- [Python](https://www.python.org/)
- [Pygame](https://www.pygame.org/) for the interface
- [python-chess](https://python-chess.readthedocs.io/) for board representation and legal move generation
