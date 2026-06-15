"""
Internationalization module for Othello.
Provides bilingual (Chinese/English) text support.
"""

from __future__ import annotations

from typing import Dict

# Language data: all game text in Chinese and English
LANG_DATA: Dict[str, Dict[str, str]] = {
    "zh": {
        "app_title": "=== 黑白棋 (Othello/Reversi) ===",
        "menu_title": "=== 主菜单 ===",
        "menu_new_game": "1. 新游戏",
        "menu_load_scores": "2. 查看历史分数",
        "menu_high_scores": "3. 高分排行榜",
        "menu_settings": "4. 设置",
        "menu_how_to_play": "5. 游戏说明",
        "menu_quit": "6. 退出",
        "menu_prompt": "请选择 (1-6): ",
        "select_mode": "=== 选择游戏模式 ===",
        "mode_vs_ai": "1. 人机对战 (VS AI)",
        "mode_2p": "2. 双人对战 (2-Player)",
        "mode_prompt": "请选择 (1-2): ",
        "current_player": "当前玩家: {player}",
        "black": "黑棋 (X)",
        "white": "白棋 (O)",
        "score": "\033[33m黑棋: {black}  白棋: {white}\033[0m",
        "valid_moves_hint": "绿色 . 表示可落子位置",
        "input_prompt": "请输入落子坐标 (如 d3)，或 h 帮助: ",
        "help_text": """
=== 帮助 ===
- 输入坐标落子，如 d3、e6（不区分大小写）
- h - 显示此帮助
- s - 显示当前分数
- u - 悔棋（撤销上一步）
- r - 重新开始
- l - 切换语言 (中文/English)
- q - 退出游戏

绿色 . 表示当前玩家可以落子的位置。
""",
        "invalid_move": "无效落子，请重新选择！",
        "invalid_input": "输入无效，请重新输入！",
        "no_moves_pass": "{player} 没有可落子的位置，跳过回合。",
        "game_over": "=== 游戏结束！===",
        "winner": "获胜者: {winner}！",
        "tie": "平局！",
        "final_score": "最终比分 - 黑棋: {black}  白棋: {white}",
        "undo_success": "已撤销上一步。",
        "undo_fail": "没有可撤销的步骤。",
        "save_success": "游戏已保存到 save.sav",
        "load_success": "已从 save.sav 加载游戏。",
        "load_fail": "没有找到存档文件 save.sav。",
        "confirm_restart": "确定重新开始？当前进度将丢失！(y/n): ",
        "confirm_quit": "确定退出？(y/n): ",
        "game_restarted": "游戏已重新开始。",
        "settings_title": "=== 设置 ===",
        "settings_difficulty": "1. 难度: {difficulty}",
        "settings_mode": "2. 游戏模式: {mode}",
        "settings_name": "3. 玩家名称: {name}",
        "settings_sound": "4. 音效: {sound}",
        "settings_language": "5. 语言: {lang}",
        "settings_back": "6. 返回主菜单",
        "settings_prompt": "请选择 (1-6): ",
        "diff_easy": "简单",
        "diff_medium": "中等",
        "diff_hard": "困难",
        "mode_ai": "人机对战",
        "mode_2p_text": "双人对战",
        "sound_on": "开",
        "sound_off": "关",
        "lang_zh": "中文",
        "lang_en": "English",
        "enter_name": "请输入玩家名称: ",
        "high_scores_title": "=== 高分排行榜 ===",
        "high_scores_empty": "暂无分数记录。",
        "high_scores_header": "排名  玩家          日期          分数  难度  胜者",
        "high_scores_row": "{rank:<6}{name:<14}{date:<14}{score:<6}{diff:<8}{winner}",
        "high_scores_back": "按 Enter 返回主菜单...",
        "load_scores_title": "=== 历史分数 ===",
        "load_scores_all": "所有历史分数记录:",
        "how_to_play": """
=== 游戏说明 ===

黑白棋 (Othello/Reversi) 规则简介：

1. 棋盘为 8×8 方格，初始时中央四格有两黑两白交叉摆放。
2. 黑棋先手，双方轮流落子。
3. 落子规则：新棋子必须夹住对方一枚或多枚棋子（横、竖、斜方向均可），
   被夹住的对方棋子翻转为己方颜色。
4. 如果一方没有合法落子位置，则跳过该方回合。
5. 当双方都无法落子或棋盘满时，游戏结束。
6. 棋子多的一方获胜。

控制键：
- 坐标落子：如 d3、e6（不区分大小写）
- h - 帮助  s - 分数  u - 悔棋
- r - 重新开始  l - 切换语言  q - 退出

AI 难度说明：
- 简单：随机选择合法位置
- 中等：贪心策略，每步尽可能多地翻转对方棋子
- 困难：使用 Minimax 深度 3 搜索 + 位置评分表评估
""",
        "ai_thinking": "AI 思考中",
        "piece_placed": "{player} 落子 {coord}",
        "flipped": "翻转了 {count} 个棋子",
        "save_prompt": "是否保存当前游戏？(y/n): ",
        "load_prompt": "检测到存档 save.sav，是否加载？(y/n): ",
        "no_save": "没有存档文件。",
        "invalid_coord": "坐标超出棋盘范围！",
        "your_turn": "轮到你了，{player}",
        "ai_turn": "AI 思考中...",
        "winner_is": "获胜者: {winner}",
        "game_draw": "平局！",
        "press_enter": "按 Enter 继续...",
    },
    "en": {
        "app_title": "=== Othello / Reversi ===",
        "menu_title": "=== Main Menu ===",
        "menu_new_game": "1. New Game",
        "menu_load_scores": "2. Load Previous Scores",
        "menu_high_scores": "3. High Scores",
        "menu_settings": "4. Settings",
        "menu_how_to_play": "5. How to Play",
        "menu_quit": "6. Quit",
        "menu_prompt": "Choose (1-6): ",
        "select_mode": "=== Select Game Mode ===",
        "mode_vs_ai": "1. VS AI",
        "mode_2p": "2. 2-Player Hotseat",
        "mode_prompt": "Choose (1-2): ",
        "current_player": "Current Player: {player}",
        "black": "Black (X)",
        "white": "White (O)",
        "score": "\033[33mBlack: {black}  White: {white}\033[0m",
        "valid_moves_hint": "Green . shows valid moves",
        "input_prompt": "Enter move coordinate (e.g. d3), or h for help: ",
        "help_text": """
=== Help ===
- Enter a coordinate to move, e.g. d3, e6 (case insensitive)
- h - Show this help
- s - Show current scores
- u - Undo last move
- r - Restart game
- l - Toggle language (English/中文)
- q - Quit game

Green . indicates valid moves for the current player.
""",
        "invalid_move": "Invalid move, please try again!",
        "invalid_input": "Invalid input, please try again!",
        "no_moves_pass": "{player} has no valid moves, turn skipped.",
        "game_over": "=== Game Over! ===",
        "winner": "Winner: {winner}!",
        "tie": "It's a tie!",
        "final_score": "Final Score - Black: {black}  White: {white}",
        "undo_success": "Last move undone.",
        "undo_fail": "No moves to undo.",
        "save_success": "Game saved to save.sav",
        "load_success": "Game loaded from save.sav.",
        "load_fail": "No save file found (save.sav).",
        "confirm_restart": "Restart? Current progress will be lost! (y/n): ",
        "confirm_quit": "Quit? (y/n): ",
        "game_restarted": "Game restarted.",
        "settings_title": "=== Settings ===",
        "settings_difficulty": "1. Difficulty: {difficulty}",
        "settings_mode": "2. Game Mode: {mode}",
        "settings_name": "3. Player Name: {name}",
        "settings_sound": "4. Sound: {sound}",
        "settings_language": "5. Language: {lang}",
        "settings_back": "6. Back to Main Menu",
        "settings_prompt": "Choose (1-6): ",
        "diff_easy": "Easy",
        "diff_medium": "Medium",
        "diff_hard": "Hard",
        "mode_ai": "VS AI",
        "mode_2p_text": "2-Player",
        "sound_on": "On",
        "sound_off": "Off",
        "lang_zh": "中文",
        "lang_en": "English",
        "enter_name": "Enter player name: ",
        "high_scores_title": "=== High Score Leaderboard ===",
        "high_scores_empty": "No scores recorded yet.",
        "high_scores_header": "Rank  Player         Date          Score  Difficulty  Winner",
        "high_scores_row": "{rank:<6}{name:<14}{date:<14}{score:<6}{diff:<12}{winner}",
        "high_scores_back": "Press Enter to return to main menu...",
        "load_scores_title": "=== Score History ===",
        "load_scores_all": "All recorded scores:",
        "how_to_play": """
=== How to Play ===

Othello / Reversi Rules:

1. The board is 8×8. The game starts with 2 black and 2 white pieces
   placed in the center in a cross pattern.
2. Black moves first, then players alternate.
3. A move must outflank one or more opponent pieces in any direction
   (horizontal, vertical, or diagonal). Outflanked pieces are flipped.
4. If a player has no valid moves, their turn is skipped.
5. The game ends when neither player can move or the board is full.
6. The player with the most pieces wins.

Controls:
- Coordinate move: e.g. d3, e6 (case insensitive)
- h - Help  s - Scores  u - Undo
- r - Restart  l - Toggle language  q - Quit

AI Difficulty:
- Easy: Random valid moves
- Medium: Greedy strategy (maximize captures each turn)
- Hard: Minimax depth 3 search + piece-square table evaluation
""",
        "ai_thinking": "AI thinking",
        "piece_placed": "{player} placed at {coord}",
        "flipped": "Flipped {count} pieces",
        "save_prompt": "Save current game? (y/n): ",
        "load_prompt": "Save file save.sav found. Load it? (y/n): ",
        "no_save": "No save file found.",
        "invalid_coord": "Coordinate out of board bounds!",
        "your_turn": "Your turn, {player}",
        "ai_turn": "AI thinking...",
        "winner_is": "Winner: {winner}",
        "game_draw": "Draw!",
        "press_enter": "Press Enter to continue...",
    },
}


class I18n:
    """Internationalization manager."""

    def __init__(self, lang: str = "zh") -> None:
        self.lang = lang

    def get(self, key: str, **kwargs) -> str:
        """Get localized text by key, formatting with kwargs."""
        text = LANG_DATA.get(self.lang, LANG_DATA["zh"]).get(key, key)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass
        return text

    def toggle(self) -> str:
        """Toggle between Chinese and English. Returns new language code."""
        self.lang = "en" if self.lang == "zh" else "zh"
        return self.lang

    def is_zh(self) -> bool:
        return self.lang == "zh"
