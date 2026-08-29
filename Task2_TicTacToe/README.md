# Task 2 - Tic-Tac-Toe AI

## Objective

To develop an interactive Tic-Tac-Toe game where a human player competes against an AI opponent.

## Technologies Used

- Python
- Streamlit
- Minimax Algorithm
- Recursion
- Game Theory

## Features

- Human vs AI gameplay
- Minimax-based AI
- Easy, Medium and Hard difficulty levels
- Score tracking
- Draw detection
- Win/loss detection
- New Game option
- Reset Scores option
- Interactive web interface

## How It Works

The player uses X and the AI uses O.

The AI uses the Minimax algorithm to evaluate possible future game states and select the best available move.

The algorithm assigns scores to game outcomes:

- AI win = +1
- Draw = 0
- Player win = -1

The AI evaluates possible moves recursively and selects the move with the highest score.

## How to Run

Install Streamlit:

```bash
pip install streamlit
Task2_TicTacToe/
├── tic_tac_toe.py
└── README.md
