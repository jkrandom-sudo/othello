# 🎮 Othello / 黑白棋 (翻转棋)

控制台版黑白棋游戏，支持 AI 对战、双人对战、多语言、保存加载等完整功能。

## 功能特点

| 功能 | 说明 |
|------|------|
| 🎯 **AI 对战** | 三档难度：简单（随机）、中等（贪心）、困难（Minimax α-β 搜索） |
| 👥 **双人对战** | 两人轮流在同一设备上下棋 |
| 🌏 **中英双语** | 按 `L` 键随时切换语言 |
| 💾 **存档/读档** | 保存游戏进度，稍后继续 |
| 📊 **排行榜** | 历史最高分排名 |
| ↩️ **悔棋** | 按 `U` 键撤销上一步 |
| 🔊 **音效** | 控制台蜂鸣音效，可开关 |
| 🎨 **彩色界面** | ANSI 颜色标记合法走法和棋盘 |

## 快速开始

```bash
cd ~/games/othello
python3 game.py
```

## 游戏操作

| 按键 | 功能 |
|------|------|
| `A1`-`H8` | 在指定位置落子（如 `d3`） |
| `H` | 显示帮助 |
| `S` | 查看分数 |
| `L` | 切换中英文语言 |
| `U` | 悔棋（撤销上一步） |
| `R` | 重新开始 |
| `Q` | 退出游戏 |
| `M` | 返回主菜单 |

### 主菜单选项

1. **新游戏** — 选择 AI 难度或双人模式，开始新游戏
2. **排行榜** — 查看历史最高分
3. **设置** — 调整难度、音效、语言
4. **帮助** — 游戏规则说明
5. **退出** — 退出游戏

## 游戏规则

- 8×8 棋盘，黑方先行（`X`），白方后手（`O`）
- 每次落子必须翻转至少一枚对方棋子
- 棋子被夹在己方棋子之间（横、竖、斜方向）则翻转
- 无合法走法时跳过回合
- 双方均无合法走法时游戏结束
- 棋子多者获胜

## 项目结构

```
~/games/othello/
├── game.py          # 主入口，游戏循环和 UI
├── board.py         # 棋盘状态、走法验证、翻转逻辑
├── ai.py            # AI 引擎（随机/贪心/Minimax）
├── i18n.py          # 中英双语国际化
├── config.py        # 配置持久化
├── scores.py        # 分数记录和排行榜
├── sound.py         # 音效模块
├── tests/
│   └── test_game.py # 61 个自动化测试
└── README.md        # 本文件
```

## AI 算法说明

| 难度 | 算法 | 说明 |
|------|------|------|
| 简单 | 随机选择 | 从合法走法中随机选一个 |
| 中等 | 贪心策略 | 每次选择翻转棋子最多的走法 |
| 困难 | Minimax + α-β 剪枝 | 深度 3 搜索，使用棋盘点位表评估 |

### 困难 AI 评估函数

`evaluate()` 综合三项指标：
- **位置价值**：使用 8×8 点位表（边角和靠近边角的位置价值高）
- **机动性**：己方与对方合法走法数量之差
- **棋子数量**：后期优势（棋盘越满权重越高）

## 运行测试

```bash
cd ~/games/othello
python3 -m pytest tests/ -v
```

61 个测试覆盖：棋盘初始化、走法验证、翻转逻辑、游戏结束检测、AI 决策、分数持久化、配置管理、国际化、悔棋、完整游戏流程。

## 技术栈

- **语言**：Python 3.11+
- **依赖**：Python 标准库（无需第三方库）
- **测试**：pytest
- **AI**：Minimax + α-β 剪枝
- **界面**：控制台字符界面 + ANSI 颜色

---

# Othello (Reversi)

A console-based Othello game with AI opponents, two-player mode, bilingual support, and full game management features.

## Quick Start

```bash
cd ~/games/othello
python3 game.py
```

## Controls

| Key | Action |
|-----|--------|
| `A1`-`H8` | Place a piece at position |
| `H` | Help |
| `S` | Show scores |
| `L` | Toggle Chinese/English |
| `U` | Undo last move |
| `R` | Restart game |
| `Q` | Quit |
| `M` | Main menu |

## AI Difficulty

| Level | Algorithm |
|-------|-----------|
| Easy | Random valid move |
| Medium | Greedy (max captures) |
| Hard | Minimax depth 3 + α-β pruning |

## Tests

```bash
pytest tests/ -v    # 61 tests
```

## Tech Stack

Python 3.11+, stdlib only, pytest, Minimax AI.
