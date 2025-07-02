# Fighting Game

A simple two-player fighting game with two modes:
- **Terminal Game:** A text-based, turn-based battle game.
- **Graphical Game:** A pygame-based graphical game with player movement and health bars.

## Project Structure

```
Game/
  README.md
  terminal_game/
    __init__.py
    entities.py         # All text-based game logic, classes, abilities, etc.
    settings.py         # Constants for the terminal game
    main.py             # Entry point for the terminal game
  pygame_game/
    __init__.py
    main.py             # Entry point for the pygame game (graphics, movement, etc.)
    settings.py         # Constants for the pygame game (screen size, colors, etc.)
    assets/
      background.png
      warrior.png
      mage.png
```

## How to Run

### Terminal Game
1. Open a terminal in the `terminal_game` folder.
2. Run:
   ```sh
   python main.py
   ```
3. Follow the prompts to play the text-based game.

### Graphical Game (pygame)
1. Open a terminal in the `pygame_game` folder.
2. Install pygame if you haven't:
   ```sh
   pip install pygame
   ```
3. Run:
   ```sh
   python main.py
   ```
4. The game will launch in fullscreen. Use **arrow keys** for Player 1 and **WASD** for Player 2. Press **Escape** or close the window to quit.

## Customization
- Edit `settings.py` in each folder to change health, speed, and other game settings.
- Replace images in `pygame_game/assets/` to use your own characters or backgrounds.

## Troubleshooting
- See comments in each `main.py` for more details.
- If images do not show in the graphical game, check the file paths in `pygame_game/main.py`.

---

Enjoy your game! If you have issues, check the troubleshooting section or ask for help. 