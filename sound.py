"""
Sound effects module using ASCII bell character.
"""

from __future__ import annotations

import sys


def _bell() -> None:
    """Print ASCII bell character."""
    print(chr(7), end="", flush=True)


def play_placement(sound_enabled: bool = True) -> None:
    """Sound for piece placement."""
    if sound_enabled:
        _bell()


def play_flip(sound_enabled: bool = True) -> None:
    """Sound for piece flip sequence (two bells)."""
    if sound_enabled:
        _bell()
        _bell()


def play_invalid(sound_enabled: bool = True) -> None:
    """Sound for invalid move (longer beep)."""
    if sound_enabled:
        _bell()


def play_game_over(sound_enabled: bool = True) -> None:
    """Sound for game over fanfare (three bells)."""
    if sound_enabled:
        _bell()
        _bell()
        _bell()
