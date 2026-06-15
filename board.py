"""
Othello (Reversi) board module.
Handles board state, move validation, flipping logic, and game-over detection.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

# Constants
BOARD_SIZE: int = 8
EMPTY: int = 0
BLACK: int = 1  # X
WHITE: int = 2  # O

PIECE_CHARS: dict[int, str] = {EMPTY: ".", BLACK: "X", WHITE: "O"}
PIECE_CHARS_COLORED: dict[int, str] = {
    EMPTY: ".",
    BLACK: "\033[97mX\033[0m",  # white X
    WHITE: "\033[90mO\033[0m",  # gray O
}

# Direction vectors: all 8 directions
DIRECTIONS: List[Tuple[int, int]] = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]

COL_LABELS: str = "ABCDEFGH"


class Board:
    """Represents an Othello board with game logic."""

    def __init__(self) -> None:
        """Initialize an 8x8 board with starting position."""
        self.grid: List[List[int]] = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        # Starting position
        self.grid[3][3] = WHITE
        self.grid[3][4] = BLACK
        self.grid[4][3] = BLACK
        self.grid[4][4] = WHITE
        self.current_player: int = BLACK  # Black goes first
        self.move_history: List[Tuple[int, int, int, List[Tuple[int, int]]]] = []
        # Stores: (row, col, player, flipped_positions)

    def clone(self) -> Board:
        """Create a deep copy of the board."""
        b = Board.__new__(Board)
        b.grid = [row[:] for row in self.grid]
        b.current_player = self.current_player
        b.move_history = list(self.move_history)
        return b

    def is_valid_coord(self, row: int, col: int) -> bool:
        """Check if coordinates are within the board."""
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def opponent(self, player: int) -> int:
        """Return the opponent piece type."""
        return WHITE if player == BLACK else BLACK

    def get_valid_moves(self, player: Optional[int] = None) -> List[Tuple[int, int]]:
        """Return list of valid (row, col) moves for the given player."""
        if player is None:
            player = self.current_player
        moves: List[Tuple[int, int]] = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.grid[r][c] == EMPTY and self._would_flip(r, c, player):
                    moves.append((r, c))
        return moves

    def _would_flip(self, row: int, col: int, player: int) -> List[Tuple[int, int]]:
        """Return list of opponent pieces that would be flipped, or empty list if invalid."""
        if self.grid[row][col] != EMPTY:
            return []
        opp = self.opponent(player)
        flipped: List[Tuple[int, int]] = []
        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            candidates: List[Tuple[int, int]] = []
            while self.is_valid_coord(r, c) and self.grid[r][c] == opp:
                candidates.append((r, c))
                r += dr
                c += dc
            if candidates and self.is_valid_coord(r, c) and self.grid[r][c] == player:
                flipped.extend(candidates)
        return flipped

    def is_valid_move(self, row: int, col: int, player: Optional[int] = None) -> bool:
        """Check if placing a piece at (row, col) is a valid move."""
        if player is None:
            player = self.current_player
        return bool(self._would_flip(row, col, player))

    def apply_move(self, row: int, col: int, player: Optional[int] = None) -> List[Tuple[int, int]]:
        """Place a piece and flip opponent pieces. Returns list of flipped positions."""
        if player is None:
            player = self.current_player
        flipped = self._would_flip(row, col, player)
        if not flipped:
            return []
        self.grid[row][col] = player
        for r, c in flipped:
            self.grid[r][c] = player
        self.move_history.append((row, col, player, list(flipped)))
        self.current_player = self.opponent(player)
        return flipped

    def undo_last_move(self) -> bool:
        """Undo the last move. Returns True if successful."""
        if not self.move_history:
            return False
        row, col, player, flipped = self.move_history.pop()
        self.grid[row][col] = EMPTY
        for r, c in flipped:
            self.grid[r][c] = self.opponent(player)
        self.current_player = player
        return True

    def get_score(self) -> Tuple[int, int]:
        """Return (black_count, white_count)."""
        black = sum(row.count(BLACK) for row in self.grid)
        white = sum(row.count(WHITE) for row in self.grid)
        return black, white

    def has_valid_moves(self, player: Optional[int] = None) -> bool:
        """Check if the player has any valid moves."""
        if player is None:
            player = self.current_player
        return len(self.get_valid_moves(player)) > 0

    def is_game_over(self) -> bool:
        """Check if the game is over (no valid moves for either player or board full)."""
        return not self.has_valid_moves(BLACK) and not self.has_valid_moves(WHITE)

    def get_winner(self) -> Optional[int]:
        """Return the winner (BLACK or WHITE), or None if tie, or None if game not over."""
        if not self.is_game_over():
            return None
        black, white = self.get_score()
        if black > white:
            return BLACK
        elif white > black:
            return WHITE
        return None  # tie

    def is_full(self) -> bool:
        """Check if the board is completely full."""
        return all(self.grid[r][c] != EMPTY for r in range(BOARD_SIZE) for c in range(BOARD_SIZE))

    def display(self, valid_moves: Optional[List[Tuple[int, int]]] = None) -> None:
        """Display the board with coordinate labels and optional valid move highlighting."""
        if valid_moves is None:
            valid_moves = []
        valid_set = set(valid_moves)

        # Top column labels
        print("   " + " ".join(COL_LABELS))
        for r in range(BOARD_SIZE):
            # Row label (1-indexed)
            print(f"{r + 1:2} ", end="")
            for c in range(BOARD_SIZE):
                if self.grid[r][c] == EMPTY and (r, c) in valid_set:
                    # Green highlight for valid moves
                    print("\033[32m.\033[0m", end=" ")
                elif self.grid[r][c] == BLACK:
                    print("\033[97mX\033[0m", end=" ")
                elif self.grid[r][c] == WHITE:
                    print("\033[90mO\033[0m", end=" ")
                else:
                    print(".", end=" ")
            print(f"{r + 1:2}")

        # Bottom column labels
        print("   " + " ".join(COL_LABELS))

    def to_dict(self) -> dict:
        """Serialize board state to a dictionary."""
        return {
            "grid": [row[:] for row in self.grid],
            "current_player": self.current_player,
            "move_history": [
                {"row": r, "col": c, "player": p, "flipped": list(f)}
                for r, c, p, f in self.move_history
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> Board:
        """Deserialize board state from a dictionary."""
        b = cls.__new__(cls)
        b.grid = [row[:] for row in data["grid"]]
        b.current_player = data["current_player"]
        b.move_history = [
            (m["row"], m["col"], m["player"], [tuple(f) for f in m["flipped"]])
            for m in data["move_history"]
        ]
        return b
