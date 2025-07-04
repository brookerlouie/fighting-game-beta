# Fighting Game (Pygame)

A turn-based two-player fighting game built with Python and pygame. Players take turns using abilities to defeat their opponent in a strategic battle featuring three unique character classes with animated sprites, customizable settings, and a modern UI.

## Project Structure

```
Game/
  main.py                  # Entry point for the graphical game
  pygame_game/
    settings.py            # Game settings and constants
    entities.py            # Character classes and ability logic
    __init__.py            # Package exports
    assets/
      tommy-background.png # Background image
      tommy-warrior.png    # Warrior character image
      Mage-idle.gif        # Mage character animated GIF
      Ghost-idle.gif       # Ghost character animated GIF
  README.md
```

## How to Run

1. Open a terminal in the `Game` directory.
2. Install required packages:
   ```sh
   pip install pygame pillow
   ```
3. Run the game:
   ```sh
   python main.py
   ```
4. The game will launch in fullscreen. Press **Escape** to pause or quit.

## Gameplay

### Character Selection
- Choose between **Warrior**, **Mage**, and **Ghost** for each player
- Customize character names
- Each class has unique abilities, stats, and visual effects
- Animated GIF sprites for Mage and Ghost characters

### Turn-Based Combat
- Players take turns using abilities
- Only the active player can use their abilities
- After using an ability, the turn switches to the other player
- Special abilities like Ghost's Confusion can grant extra turns
- No movement - focus on strategic ability usage

### Controls

#### Game Controls
- **Escape**: Pause/Resume game or quit (when game over)
- **Mouse**: Click menu options in pause/settings menus

#### Player Abilities
- **Player 1** (always uses these keys):
  - **Q**: Ability 1 (Light Attack)
  - **W**: Ability 2 (Heavy Strike/Fireball/Slash)
  - **E**: Ability 3 (Block/Heal/Confusion)
  - **R**: Ability 4 (Health Potion/Souls)

- **Player 2** (always uses these keys):
  - **U**: Ability 1 (Light Attack)
  - **I**: Ability 2 (Heavy Strike/Fireball/Slash)
  - **O**: Ability 3 (Block/Heal/Confusion)
  - **P**: Ability 4 (Health Potion/Souls)

Regardless of which class or side, Player 1 always uses Q/W/E/R and Player 2 always uses U/I/O/P for their abilities. The on-screen UI dynamically shows the correct keys and ability names for each player.

### Character Classes

#### Warrior
- **Health:** 120 HP
- **Abilities:**
  - **Light Attack (Q/U):** Quick, reliable attack (10-14 damage)
  - **Heavy Strike (W/I):** Powerful melee attack with 25% chance to stun (20 damage normally, 30 damage when stun occurs)
  - **Block (E/O):** Block the next attack
  - **Health Potion (R/P):** Restore 30 HP

#### Mage
- **Health:** 80 HP
- **Abilities:**
  - **Light Attack (Q/U):** Quick, reliable attack (10-14 damage)
  - **Fireball (W/I):** Fiery magical attack with 25% chance to poison (20-25 damage, poison deals 1-5 damage per turn for 3 turns)
  - **Heal (E/O):** Restore 25 HP to yourself
  - **Health Potion (R/P):** Restore 30 HP
- **Special:** Animated GIF sprite

#### Ghost
- **Health:** 100 HP
- **Abilities:**
  - **Light Attack (Q/U):** Quick, reliable attack (10-14 damage)
  - **Slash (W/I):** Powerful slash with 25% chance to cause bleeding (15-20 damage)
  - **Confusion (E/O):** Confusing attack that deals 10 damage with 20% chance to grant an extra turn
  - **Souls (R/P):** Steal the enemy's soul and heal yourself for 30 HP
- **Special:** Animated GIF sprite and unique extra turn mechanic

### Status Effects

- **Stunned:** Applied by Warrior's Heavy Strike. Target misses their next turn
- **Poisoned:** Applied by Mage's Fireball. Target takes 1-5 damage per turn for 3 turns
- **Bleeding:** Applied by Ghost's Slash. Target takes 1 damage per turn for 5 turns

### Dynamic UI

- Health bars, character names, and ability keys are displayed on the same side as each character
- UI automatically adjusts based on character positions
- Active player's abilities are highlighted in yellow
- Inactive player's abilities are shown in gray
- FPS counter displayed underneath the left health bar
- Turn indicator shows whose turn it is with colored borders around active player

## Settings & Customization

### Pause Menu
- Press **Escape** during gameplay to access the pause menu
- Options include:
  - **Settings**: Access brightness, resolution, and display options
  - **Exit Game**: Quit the game

### Settings Menu
- **Brightness Control**: Adjust game brightness from 0% to 150%
- **Resolution Options**: Choose from multiple resolutions and FPS:
  - 800x600 @ 60fps
  - 1024x768 @ 60fps
  - 1280x720 @ 60fps
  - 1280x720 @ 120fps
  - 1920x1080 @ 60fps
  - 1920x1080 @ 120fps
  - 1920x1080 @ 144fps
- **Fullscreen Toggle**: Switch between fullscreen and windowed mode
- Changes apply immediately and persist between game sessions

### Navigation Controls
- **W/S** or **Up/Down**: Navigate menu options
- **Enter**: Select/apply option
- **Escape**: Go back to previous menu
- **Mouse**: Click menu options

## Technical Features

### Animated GIF Support
- Mage and Ghost characters use animated GIF sprites
- Smooth animation in both character selection and in-game
- Uses Pillow library for GIF frame extraction
- Fallback to static images if GIFs are unavailable

### Advanced Ability System
- Status effects with duration tracking
- Extra turn mechanics (Ghost's Confusion)
- Blocking system to counter attacks
- Dynamic targeting based on character class

### Performance Monitoring
- Real-time FPS counter
- Smooth frame rate tracking
- Optimized rendering for different resolutions

### Display Management
- Dynamic resolution switching
- Fullscreen/windowed mode support
- Brightness adjustment with real-time preview
- Background scaling for different resolutions

## Customization
- Edit `pygame_game/settings.py` to change health, damage values, and other game settings
- Replace images in `pygame_game/assets/` to use your own characters or backgrounds
- Add animated GIFs for new character classes
- Modify `pygame_game/entities.py` to add new abilities or character classes

## Troubleshooting
- If images do not show in the graphical game, check the file paths in `main.py` and ensure your images are in `pygame_game/assets/`
- If you see errors about missing modules, make sure you installed pygame and pillow:
  ```sh
  pip install pygame pillow
  ```
- For animated GIFs, ensure the Pillow library is installed for proper frame extraction
- If resolution changes don't apply, try restarting the game
- For performance issues, try lowering the resolution or FPS in the settings menu

---

## Creators

**Coder:** Louie Brooker  
Business email: brookerlouie7@gmail.com

**Artist:** Tommy Batchelor  
Business email: tommybatchelor986@gmail.com

Enjoy your turn-based battle! If you have issues, check the troubleshooting section or ask for help. 