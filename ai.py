"""
AI module for Othello.
Provides three difficulty levels: Easy (random), Medium (greedy), Hard (minimax + piece-square).
"""

from __future__ import annotations

import random
import time
from typing import List, Optional, Tuple

from board import BOARD_SIZE, BLACK, WHITE, EMPTY, Board, DIRECTIONS

# Optional i18n instance for AI messages
_i18n = None

def set_i18n(i18n_instance) -> None:
    """Set the i18n instance for AI messages."""
    global _i18n
    _i18n = i18n_instance

# Piece-square table for positional evaluation (8x8, from black's perspective)
# Higher values = better positions
PIECE_SQUARE: List[List[int]] = [
    [ 100, -20,  10,   5,   5,  10, -20,  100],
    [ -20, -50,  -2,  -2,  -2,  -2, -50,  -20],
    [  10,  -2,   1,   1,   1,   1,  -2,   10],
    [   5,  -2,   1,   0,   0,   1,  -2,    5],
    [   5,  -2,   1,   0,   0,   1,  -2,    5],
    [  10,  -2,   1,   1,   1,   1,  -2,   10],
    [ -20, -50,  -2,  -2,  -2,  -2, -50,  -20],
    [ 100, -20,  10,   5,   5,  10, -20,  100],
]


def get_easy_move(board: Board, player: int) -> Optional[Tuple[int, int]]:
    """Easy AI: pick a random valid move."""
    moves = board.get_valid_moves(player)
    if not moves:
        return None
    return random.choice(moves)


def get_medium_move(board: Board, player: int) -> Optional[Tuple[int, int]]:
    """Medium AI: greedy strategy — maximize pieces captured this turn."""
    moves = board.get_valid_moves(player)
    if not moves:
        return None
    best_move = moves[0]
    best_score = -1
    for r, c in moves:
        flipped = board._would_flip(r, c, player)
        if len(flipped) > best_score:
            best_score = len(flipped)
            best_move = (r, c)
    return best_move


def get_hard_move(board: Board, player: int) -> Optional[Tuple[int, int]]:
    """Hard AI: minimax search with depth 3 and piece-square evaluation."""
    moves = board.get_valid_moves(player)
    if not moves:
        return None

    _, best_move = minimax(board, player, depth=3, alpha=-float("inf"), beta=float("inf"), maximizing=True)
    if best_move is None:
        return random.choice(moves)
    return best_move


def evaluate(board: Board, player: int) -> float:
    """
    Evaluate board position from the given player's perspective.
    Uses piece-square table + mobility + piece count.
    """
    opp = WHITE if player == BLACK else BLACK
    score = 0.0

    # Piece-square positional score
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board.grid[r][c] == player:
                score += PIECE_SQUARE[r][c]
            elif board.grid[r][c] == opp:
                score -= PIECE_SQUARE[r][c]

    # Mobility (number of valid moves) — weighted
    player_moves = len(board.get_valid_moves(player))
    opp_moves = len(board.get_valid_moves(opp))
    if player_moves + opp_moves > 0:
        mobility = 10 * (player_moves - opp_moves) / (player_moves + opp_moves)
        score += mobility

    # Piece count differential (late game emphasis)
    player_count = sum(row.count(player) for row in board.grid)
    opp_count = sum(row.count(opp) for row in board.grid)
    total = player_count + opp_count
    if total > 0:
        # Weight increases as board fills up
        parity_weight = total / 64.0 * 20
        score += parity_weight * (player_count - opp_count) / total

    return score


def minimax(
    board: Board,
    player: int,
    depth: int,
    alpha: float,
    beta: float,
    maximizing: bool,
) -> Tuple[float, Optional[Tuple[int, int]]]:
    """
    Minimax with alpha-beta pruning.
    Returns (evaluation_score, best_move).
    """
    if depth == 0 or board.is_game_over():
        return evaluate(board, player), None

    moves = board.get_valid_moves(player)
    if not moves:
        # No moves — pass turn
        opp = WHITE if player == BLACK else BLACK
        if not board.has_valid_moves(opp):
            # Neither player can move — game over
            return evaluate(board, player), None
        # Pass: switch player
        b2 = board.clone()
        b2.current_player = opp
        score, _ = minimax(b2, opp, depth - 1, alpha, beta, not maximizing)
        return score, None

    best_move: Optional[Tuple[int, int]] = None

    if maximizing:
        max_eval = -float("inf")
        # Sort moves: try greedy-first ordering for better pruning
        moves_sorted = sorted(moves, key=lambda m: len(board._would_flip(m[0], m[1], player)), reverse=True)
        for r, c in moves_sorted:
            b2 = board.clone()
            b2.apply_move(r, c, player)
            eval_score, _ = minimax(b2, WHITE if player == BLACK else BLACK, depth - 1, alpha, beta, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (r, c)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        moves_sorted = sorted(moves, key=lambda m: len(board._would_flip(m[0], m[1], player)), reverse=True)
        for r, c in moves_sorted:
            b2 = board.clone()
            b2.apply_move(r, c, player)
            eval_score, _ = minimax(b2, WHITE if player == BLACK else BLACK, depth - 1, alpha, beta, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (r, c)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move


def get_ai_move(board: Board, player: int, difficulty: str) -> Optional[Tuple[int, int]]:
    """
    Get an AI move based on difficulty level.
    Shows a brief thinking animation (dots...).
    """
    thinking_msg = _i18n.get("ai_thinking") if _i18n else "AI thinking"
    print(thinking_msg, end="", flush=True)
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print()

    if difficulty == "easy":
        return get_easy_move(board, player)
    elif difficulty == "medium":
        return get_medium_move(board, player)
    elif difficulty == "hard":
        return get_hard_move(board, player)
    else:
        return get_easy_move(board, player)
