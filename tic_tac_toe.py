import streamlit as st
import random

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Tic-Tac-Toe AI",
    page_icon="🎮",
    layout="centered"
)

# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown("""
<style>
    .title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
    }

    .subtitle {
        text-align: center;
        color: #777;
        margin-bottom: 25px;
    }

    .winner {
        text-align: center;
        font-size: 25px;
        font-weight: bold;
        padding: 15px;
    }

    .board-info {
        text-align: center;
        font-size: 18px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "board" not in st.session_state:
    st.session_state.board = [""] * 9

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "winner" not in st.session_state:
    st.session_state.winner = None

if "player_score" not in st.session_state:
    st.session_state.player_score = 0

if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0

if "draw_score" not in st.session_state:
    st.session_state.draw_score = 0


# ============================================================
# GAME FUNCTIONS
# ============================================================

def check_winner(board):
    winning_combinations = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    for a, b, c in winning_combinations:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    if "" not in board:
        return "Draw"

    return None


def available_moves(board):
    return [i for i, cell in enumerate(board) if cell == ""]


# ============================================================
# MINIMAX ALGORITHM
# ============================================================

def minimax(board, maximizing):
    result = check_winner(board)

    if result == "O":
        return 1

    if result == "X":
        return -1

    if result == "Draw":
        return 0

    if maximizing:
        best_score = float("-inf")

        for move in available_moves(board):
            board[move] = "O"
            score = minimax(board, False)
            board[move] = ""
            best_score = max(best_score, score)

        return best_score

    else:
        best_score = float("inf")

        for move in available_moves(board):
            board[move] = "X"
            score = minimax(board, True)
            board[move] = ""
            best_score = min(best_score, score)

        return best_score


def find_best_move(board):
    best_score = float("-inf")
    best_move = None

    for move in available_moves(board):
        board[move] = "O"

        score = minimax(board, False)

        board[move] = ""

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


# ============================================================
# AI MOVE
# ============================================================

def make_ai_move():
    board = st.session_state.board

    if st.session_state.game_over:
        return

    if "" not in board:
        return

    difficulty = st.session_state.difficulty

    if difficulty == "Easy":
        move = random.choice(available_moves(board))

    elif difficulty == "Medium":
        if random.random() < 0.5:
            move = random.choice(available_moves(board))
        else:
            move = find_best_move(board)

    else:
        move = find_best_move(board)

    if move is not None:
        board[move] = "O"

    check_game_status()


# ============================================================
# GAME STATUS
# ============================================================

def check_game_status():

    result = check_winner(st.session_state.board)

    if result is None:
        return

    st.session_state.game_over = True
    st.session_state.winner = result

    if result == "X":
        st.session_state.player_score += 1

    elif result == "O":
        st.session_state.ai_score += 1

    elif result == "Draw":
        st.session_state.draw_score += 1


# ============================================================
# PLAYER MOVE
# ============================================================

def player_move(position):

    if st.session_state.game_over:
        return

    board = st.session_state.board

    if board[position] != "":
        return

    board[position] = "X"

    check_game_status()

    if not st.session_state.game_over:
        make_ai_move()


# ============================================================
# RESET GAME
# ============================================================

def reset_game():

    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.session_state.winner = None


def reset_scores():

    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.session_state.draw_score = 0
    reset_game()


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="title">🎮 Tic-Tac-Toe AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Play against an AI powered by the Minimax algorithm'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Game Settings")

    difficulty = st.selectbox(
        "AI Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    st.session_state.difficulty = difficulty

    st.divider()

    st.subheader("📊 Scoreboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("You", st.session_state.player_score)

    with col2:
        st.metric("AI", st.session_state.ai_score)

    with col3:
        st.metric("Draws", st.session_state.draw_score)

    st.divider()

    st.info(
        "You are ❌\n\n"
        "AI is ⭕\n\n"
        "The Hard mode uses the Minimax algorithm."
    )

    if st.button(
        "🔄 New Game",
        use_container_width=True
    ):
        reset_game()
        st.rerun()

    if st.button(
        "🗑️ Reset Scores",
        use_container_width=True
    ):
        reset_scores()
        st.rerun()


# ============================================================
# GAME STATUS MESSAGE
# ============================================================

if st.session_state.winner == "X":

    st.success("🎉 You won!")

elif st.session_state.winner == "O":

    st.error("🤖 AI won! Try again.")

elif st.session_state.winner == "Draw":

    st.warning("🤝 It's a draw!")

else:

    st.markdown(
        '<div class="board-info">Your turn — choose a square!</div>',
        unsafe_allow_html=True
    )


# ============================================================
# GAME BOARD
# ============================================================

symbols = {
    "X": "❌",
    "O": "⭕",
    "": " "
}

for row in range(3):

    columns = st.columns(3)

    for col in range(3):

        position = row * 3 + col
        value = st.session_state.board[position]

        with columns[col]:

            if st.button(
                symbols[value],
                key=f"cell_{position}",
                use_container_width=True,
                disabled=(
                    value != ""
                    or st.session_state.game_over
                )
            ):

                player_move(position)
                st.rerun()


# ============================================================
# GAME INFORMATION
# ============================================================

st.divider()

with st.expander("🧠 How the AI works"):

    st.markdown("""
    ### Minimax Algorithm

    The AI evaluates possible future moves and assigns
    scores to different game outcomes.

    **Winning move → +1**

    **Draw → 0**

    **Losing move → -1**

    The AI explores possible moves recursively and chooses
    the move with the best possible outcome.

    ### Game Flow

    ```text
    Player makes a move
            ↓
    Check game status
            ↓
    AI examines possible moves
            ↓
    Minimax evaluates game states
            ↓
    AI selects the best move
            ↓
    Board updates
            ↓
    Continue until win/draw
    ```
    """)


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "Task 2 — Tic-Tac-Toe AI | "
    "Python + Streamlit + Minimax"
)