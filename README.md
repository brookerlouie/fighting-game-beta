# Fighting Game

A simple two-player fighting game built with Python and pygame.

## Prerequisites

- **Python 3.8+** (recommended)
- **pip** (comes with Python)
- **pygame**
- (Optional) **Git** for version control

## Setup Instructions (Windows)

1. **Clone or Download the Repository**
   - If using Git:
     ```sh
     git clone <repo-url>
     cd Game
     ```
   - Or download and unzip the project, then open a terminal in the `Game` folder.

2. **Install Python Dependencies**
   - Open Command Prompt or PowerShell in the `Game` directory.
   - Install pygame:
     ```sh
     pip install pygame
     ```

3. **Add Your Images (Optional)**
   - Place your background and character images in `game/assets/`:
     - `background.png`
     - `warrior.png`
     - `mage.png`
   - If these files are missing, the game will use colored rectangles and a solid background.

4. **Run the Game**
   - In the `Game` directory, run:
     ```sh
     python main.py
     ```
   - The game will launch in fullscreen. Use **arrow keys** for Player 1 and **WASD** for Player 2.
   - Press **Escape** or close the window to quit.

## Troubleshooting

- **Images not showing?**
  - Make sure your images are in `game/assets/` and match the filenames in the code.
  - If using absolute paths, update them in `main.py` to match your system.
- **'git' is not recognized?**
  - Install Git from [git-scm.com](https://git-scm.com/download/win) and add it to your PATH.
- **'pygame' is not recognized?**
  - Make sure you installed pygame with `pip install pygame`.
- **Game window is too large or too small?**
  - The game uses your current screen resolution in fullscreen mode.

## Controls

- **Player 1:** Arrow keys (← ↑ → ↓)
- **Player 2:** WASD
- **Quit:** Escape key or close the window

## Customization

- Edit `game/settings.py` to change health, speed, and other game settings.
- Replace images in `game/assets/` to use your own characters or backgrounds.

---

Enjoy your game! If you have issues, check the troubleshooting section or ask for help. 