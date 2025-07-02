# Fighting Game (Pygame)

A simple two-player fighting game built with Python and pygame.

## Project Structure

```
Game/
  main.py                  # Entry point for the graphical game
  pygame_game/
    settings.py            # Game settings and constants
    entities.py            # Character classes and logic
    assets/
      background.png       # Background image
      warrior.png          # Warrior character image
      mage.png             # Mage character image
  README.md
```

## How to Run

1. Open a terminal in the `Game` directory.
2. Install pygame if you haven't:
   ```sh
   pip install pygame
   ```
3. Run the game:
   ```sh
   python main.py
   ```
4. The game will launch in fullscreen. Use **arrow keys** for Player 1 and **WASD** for Player 2. Press **Escape** or close the window to quit.

## Customization
- Edit `pygame_game/settings.py` to change health, speed, and other game settings.
- Replace images in `pygame_game/assets/` to use your own characters or backgrounds.

## Troubleshooting
- If images do not show in the graphical game, check the file paths in `main.py` and ensure your images are in `pygame_game/assets/`.
- If you see errors about missing modules, make sure you installed pygame with `pip install pygame`.

---

Enjoy your game! If you have issues, check the troubleshooting section or ask for help. 