"""
Othello (Reversi) - Main game entry point.
Handles the game loop, menu system, settings, and user interaction.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, Optional, Tuple

from board import BOARD_SIZE, BLACK, WHITE, EMPTY, Board, COL_LABELS
from ai import get_ai_move
from config import load_config, save_config
from i18n import I18n
from scores import load_scores, add_score, get_top_scores
from sound import play_placement, play_flip, play_invalid, play_game_over

SAVE_FILE = "save.sav"


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def print_header(i18n: I18n) -> None:
    """Print the game title header."""
    print("\033[36m" + i18n.get("app_title") + "\033[0m")
    print()


def show_menu(i18n: I18n) -> str:
    """Display the main menu and return the user's choice."""
    clear_screen()
    print_header(i18n)
    print(i18n.get("menu_title"))
    print(i18n.get("menu_new_game"))
    print(i18n.get("menu_load_scores"))
    print(i18n.get("menu_high_scores"))
    print(i18n.get("menu_settings"))
    print(i18n.get("menu_how_to_play"))
    print(i18n.get("menu_quit"))
    return input(i18n.get("menu_prompt")).strip()


def show_settings(config: Dict[str, Any], i18n: I18n) -> None:
    """Display and handle the settings menu."""
    while True:
        clear_screen()
        print_header(i18n)
        print(i18n.get("settings_title"))

        diff_key = f"diff_{config['difficulty']}"
        mode_key = "mode_ai" if config["mode"] == "ai" else "mode_2p_text"
        sound_str = i18n.get("sound_on") if config["sound"] else i18n.get("sound_off")
        lang_str = i18n.get("lang_zh") if i18n.is_zh() else i18n.get("lang_en")

        print(i18n.get("settings_difficulty", difficulty=i18n.get(diff_key)))
        print(i18n.get("settings_mode", mode=i18n.get(mode_key)))
        print(i18n.get("settings_name", name=config["player_name"]))
        print(i18n.get("settings_sound", sound=sound_str))
        print(i18n.get("settings_language", lang=lang_str))
        print(i18n.get("settings_back"))

        choice = input(i18n.get("settings_prompt")).strip()

        if choice == "1":
            # Cycle difficulty
            diffs = ["easy", "medium", "hard"]
            idx = diffs.index(config["difficulty"]) if config["difficulty"] in diffs else 0
            config["difficulty"] = diffs[(idx + 1) % len(diffs)]
            save_config(config)
        elif choice == "2":
            # Toggle game mode
            config["mode"] = "2p" if config["mode"] == "ai" else "ai"
            save_config(config)
        elif choice == "3":
            # Change player name
            name = input(i18n.get("enter_name")).strip()
            if name:
                config["player_name"] = name
                save_config(config)
        elif choice == "4":
            # Toggle sound
            config["sound"] = not config["sound"]
            save_config(config)
        elif choice == "5":
            # Toggle language
            i18n.toggle()
            config["language"] = i18n.lang
            save_config(config)
        elif choice == "6":
            break
        else:
            print(i18n.get("invalid_input"))
            input(i18n.get("press_enter"))


def show_high_scores(i18n: I18n) -> None:
    """Display the high score leaderboard."""
    clear_screen()
    print_header(i18n)
    print(i18n.get("high_scores_title"))
    print()

    top_scores = get_top_scores(10)
    if not top_scores:
        print(i18n.get("high_scores_empty"))
    else:
        print(i18n.get("high_scores_header"))
        print("-" * 60)
        for rank, s in enumerate(top_scores, 1):
            name = s.get("player_name", "?")
            date = s.get("date", "?")
            score = str(s.get("score", 0))
            diff = s.get("difficulty", "?")
            winner = s.get("winner", "?")
            print(i18n.get("high_scores_row", rank=rank, name=name, date=date, score=score, diff=diff, winner=winner))

    print()
    input(i18n.get("high_scores_back"))


def show_previous_scores(i18n: I18n) -> None:
    """Display all previous scores."""
    clear_screen()
    print_header(i18n)
    print(i18n.get("load_scores_title"))
    print()
    print(i18n.get("load_scores_all"))
    print()

    scores = load_scores()
    if not scores:
        print(i18n.get("high_scores_empty"))
    else:
        print(i18n.get("high_scores_header"))
        print("-" * 60)
        for rank, s in enumerate(scores, 1):
            name = s.get("player_name", "?")
            date = s.get("date", "?")
            score = str(s.get("score", 0))
            diff = s.get("difficulty", "?")
            winner = s.get("winner", "?")
            print(i18n.get("high_scores_row", rank=rank, name=name, date=date, score=score, diff=diff, winner=winner))

    print()
    input(i18n.get("high_scores_back"))


def show_how_to_play(i18n: I18n) -> None:
    """Display the how-to-play instructions."""
    clear_screen()
    print_header(i18n)
    print(i18n.get("how_to_play"))
    print()
    input(i18n.get("press_enter"))


def parse_coord(input_str: str) -> Optional[Tuple[int, int]]:
    """Parse a coordinate string like 'd3' into (row, col). Returns None if invalid."""
    input_str = input_str.strip().lower()
    if len(input_str) < 2:
        return None
    col_char = input_str[0]
    if col_char not in "abcdefgh":
        return None
    col = ord(col_char) - ord("a")
    try:
        row = int(input_str[1:]) - 1
    except ValueError:
        return None
    if row < 0 or row >= BOARD_SIZE:
        return None
    return row, col


def get_player_name(player: int, config: Dict[str, Any], i18n: I18n) -> str:
    """Get display name for a player."""
    if player == BLACK:
        return i18n.get("black")
    else:
        if config["mode"] == "2p":
            return i18n.get("white")
        else:
            return "AI"


def save_game_state(board: Board, config: Dict[str, Any], i18n: I18n) -> None:
    """Save the current game state to save.sav."""
    data = {
        "board": board.to_dict(),
        "config": config,
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(i18n.get("save_success"))


def load_game_state(i18n: I18n) -> Optional[Tuple[Board, Dict[str, Any]]]:
    """Load game state from save.sav. Returns (board, config) or None."""
    if not os.path.exists(SAVE_FILE):
        print(i18n.get("load_fail"))
        return None
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        board = Board.from_dict(data["board"])
        config = data.get("config", load_config())
        print(i18n.get("load_success"))
        return board, config
    except (json.JSONDecodeError, IOError, KeyError):
        print(i18n.get("load_fail"))
        return None


def game_loop(board: Board, config: Dict[str, Any], i18n: I18n) -> None:
    """
    Main game loop.
    Handles turns, input, AI moves, undo, and game-over detection.
    """
    sound_enabled = config.get("sound", True)

    while not board.is_game_over():
        player = board.current_player
        player_name = get_player_name(player, config, i18n)

        # Check if current player has valid moves
        valid_moves = board.get_valid_moves(player)
        if not valid_moves:
            # Pass turn
            print()
            print(i18n.get("no_moves_pass", player=player_name))
            board.current_player = board.opponent(player)
            input(i18n.get("press_enter"))
            continue

        # Display board
        clear_screen()
        print_header(i18n)

        # Show current player with red color
        print(f"\033[31m{i18n.get('current_player', player=player_name)}\033[0m")
        print(i18n.get("score", black=board.get_score()[0], white=board.get_score()[1]))
        print(i18n.get("valid_moves_hint"))
        print()

        board.display(valid_moves=valid_moves)
        print()

        if config["mode"] == "ai" and player == WHITE:
            # AI's turn
            print(i18n.get("ai_turn"))
            move = get_ai_move(board, player, config["difficulty"])
            if move is None:
                continue
            r, c = move
            flipped = board.apply_move(r, c, player)
            coord_str = f"{COL_LABELS[c]}{r + 1}"
            print(i18n.get("piece_placed", player=player_name, coord=coord_str))
            print(i18n.get("flipped", count=len(flipped)))
            play_placement(sound_enabled)
            if flipped:
                play_flip(sound_enabled)
            input(i18n.get("press_enter"))
        else:
            # Human's turn
            cmd = input(i18n.get("input_prompt")).strip().lower()

            if cmd == "q":
                # Quit
                confirm = input(i18n.get("confirm_quit")).strip().lower()
                if confirm in ("y", "yes", "是"):
                    # Ask to save
                    save_choice = input(i18n.get("save_prompt")).strip().lower()
                    if save_choice in ("y", "yes", "是"):
                        save_game_state(board, config, i18n)
                    return
                continue

            if cmd == "r":
                confirm = input(i18n.get("confirm_restart")).strip().lower()
                if confirm in ("y", "yes", "是"):
                    return  # Return to menu (caller will restart)
                continue

            if cmd == "h":
                print(i18n.get("help_text"))
                input(i18n.get("press_enter"))
                continue

            if cmd == "s":
                print(i18n.get("score", black=board.get_score()[0], white=board.get_score()[1]))
                input(i18n.get("press_enter"))
                continue

            if cmd == "u":
                if board.undo_last_move():
                    print(i18n.get("undo_success"))
                    input(i18n.get("press_enter"))
                else:
                    print(i18n.get("undo_fail"))
                    input(i18n.get("press_enter"))
                continue

            if cmd == "l":
                i18n.toggle()
                config["language"] = i18n.lang
                save_config(config)
                continue

            # Try to parse as coordinate
            coord = parse_coord(cmd)
            if coord is None:
                print(i18n.get("invalid_input"))
                play_invalid(sound_enabled)
                input(i18n.get("press_enter"))
                continue

            r, c = coord
            if not board.is_valid_move(r, c, player):
                print(i18n.get("invalid_move"))
                play_invalid(sound_enabled)
                input(i18n.get("press_enter"))
                continue

            # Valid move
            flipped = board.apply_move(r, c, player)
            coord_str = f"{COL_LABELS[c]}{r + 1}"
            play_placement(sound_enabled)
            if flipped:
                play_flip(sound_enabled)

    # Game over
    clear_screen()
    print_header(i18n)
    print(i18n.get("game_over"))
    print()

    black_score, white_score = board.get_score()
    print(i18n.get("final_score", black=black_score, white=white_score))
    print()

    winner = board.get_winner()
    if winner is not None:
        winner_name = i18n.get("black") if winner == BLACK else i18n.get("white")
        print(i18n.get("winner", winner=winner_name))
        winner_str = winner_name
    else:
        print(i18n.get("tie"))
        winner_str = i18n.get("tie")

    play_game_over(sound_enabled)

    # Save score
    player_score = black_score if winner == BLACK else white_score
    if config["mode"] == "ai":
        # Record the human player's score
        add_score(
            player_name=config["player_name"],
            score=player_score,
            difficulty=config["difficulty"],
            winner=winner_str,
        )
    else:
        # In 2P mode, record both players
        add_score(
            player_name=i18n.get("black"),
            score=black_score,
            difficulty="2P",
            winner=winner_str,
        )
        add_score(
            player_name=i18n.get("white"),
            score=white_score,
            difficulty="2P",
            winner=winner_str,
        )

    print()
    input(i18n.get("press_enter"))


def start_game(config: Dict[str, Any], i18n: I18n) -> None:
    """Start a new game."""
    board = Board()
    game_loop(board, config, i18n)


def main() -> None:
    """Main entry point."""
    config = load_config()
    i18n = I18n(config.get("language", "zh"))

    while True:
        choice = show_menu(i18n)

        if choice == "1":
            # New Game
            # Check for save file
            if os.path.exists(SAVE_FILE):
                load_choice = input(i18n.get("load_prompt")).strip().lower()
                if load_choice in ("y", "yes", "是"):
                    result = load_game_state(i18n)
                    if result is not None:
                        board, loaded_config = result
                        config.update(loaded_config)
                        game_loop(board, config, i18n)
                        continue
            start_game(config, i18n)

        elif choice == "2":
            show_previous_scores(i18n)

        elif choice == "3":
            show_high_scores(i18n)

        elif choice == "4":
            show_settings(config, i18n)

        elif choice == "5":
            show_how_to_play(i18n)

        elif choice == "6":
            clear_screen()
            print(i18n.get("app_title"))
            print()
            print(i18n.get("confirm_quit"))
            confirm = input().strip().lower()
            if confirm in ("y", "yes", "是", ""):
                sys.exit(0)

        else:
            print(i18n.get("invalid_input"))
            input(i18n.get("press_enter"))


if __name__ == "__main__":
    main()
