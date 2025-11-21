# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a pygame-based educational game called "Gluttonous Boy" where a player collects falling food items. The objective is to collect healthy foods (positive points) while avoiding unhealthy foods (negative points) within a 60-second time limit.

## Running the Game

```bash
python main.py
```

Requirements: pygame (install with `pip install pygame`)

## Architecture

### Core Structure

The game follows a classic pygame architecture with three main modules:

- **main.py**: Game loop and core game logic (Game class)
- **sprites.py**: All game entities (Player, Food, FloatingText sprite classes)
- **settings.py**: Configuration constants (screen dimensions, colors, speeds, scoring)

### Game Flow

1. Game instance created → `show_start_screen()` displays instructions
2. User presses key → `new()` initializes game state and calls `run()`
3. `run()` executes main game loop: `events()` → `update()` → `draw()`
4. Game ends when score ≤ -20 or 60 seconds elapse → `show_go_screen()`
5. Loop repeats until user closes window

### Sprite System

The game uses pygame's sprite groups for entity management:

- `all_sprites`: Contains all visible sprites (player, food, floating text)
- `foods`: Subset tracking only food items for collision detection
- `texts`: Subset tracking floating score indicators

**Player**: Controlled with arrow keys, confined to screen boundaries, positioned above ground

**Food**: Spawns every 1000ms at random x-position above screen, falls at random speed (3-7), categorized as 'healthy' (+10 points) or 'unhealthy' (-5 points)

**FloatingText**: Score indicators that float upward for 60 frames then disappear

### Visual Layers (draw order)

1. Sky blue background
2. Ground surface (tiled from Terreno_01.png)
3. All sprites (player + food)
4. Floating text overlays
5. HUD (score + time remaining)

## Asset Structure

All game assets live in `assets/` directory:

- **Player**: Boneco_Gordinho_A1.png
- **Healthy foods**: Alface.png, Banana.png, Maçã.png, Pêra.png
- **Unhealthy foods**: Chocolate.png, Hamburguer.png, Refrigerante.png, Sorvete.png
- **Ground tiles**: Terreno_01.png, Terreno_02.png, Terreno_03.png (only #1 currently used)

Images are loaded using `os.path.join(ASSETS_DIR, filename)` for cross-platform compatibility.

## Key Configuration Values

Defined in settings.py:

- **Gameplay**: 60s duration, spawn rate 1000ms, player speed 5px/frame
- **Scoring**: Healthy +10, Unhealthy -5, lose at -20
- **Sizing**: Screen 800x600, food 45x45, player 50x50, ground height 100px
- **Food falling speed**: Random between 3-7 px/frame

## Development Notes

- The game uses Comic Sans MS font (fallback to system default if unavailable)
- Ground is tiled horizontally by blitting the ground image repeatedly across screen width
- Player sprite has a +20px vertical offset to create slight visual overlap with ground
- Food items spawn off-screen (y: -100 to -40) and are killed when they fall below screen
- Text shadows are rendered by drawing black text offset +2px in both x and y before drawing colored text
