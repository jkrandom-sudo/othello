"""
Configuration persistence module.
Saves/loads game settings from config.json.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict

CONFIG_FILE = "config.json"

DEFAULT_CONFIG: Dict[str, Any] = {
    "difficulty": "easy",
    "mode": "ai",  # "ai" or "2p"
    "player_name": "玩家",
    "sound": True,
    "language": "zh",
}


def load_config() -> Dict[str, Any]:
    """Load configuration from config.json, falling back to defaults."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Merge with defaults to ensure all keys exist
            config = DEFAULT_CONFIG.copy()
            config.update(data)
            return config
        except (json.JSONDecodeError, IOError):
            pass
    return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to config.json."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
