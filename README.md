# Fantasy Fight - Turn-Based Fighting Game

A turn-based two-player fighting game built with Python and pygame. Players take turns using abilities to defeat their opponent in a strategic battle featuring three unique character classes with animated sprites, customizable settings, multiplayer support with character selection, and a modern UI.

## 📋 Quick Navigation

- [How to Run](#how-to-run)
- [Game Modes](#game-modes)
- [Multiplayer Features](#multiplayer-features)
- [Character Classes](#character-classes)
- [Settings & Customization](#settings--customization)
- [Troubleshooting](#troubleshooting)
- **[📖 Detailed Multiplayer Guide](MULTIPLAYER_README.md)**

## Project Structure

```
Game/
  main.py                  # Entry point for the graphical game
  multiplayer.py           # Multiplayer client and server logic
  multiplayer_ui.py        # Multiplayer user interface
  lobby_server.py          # Standalone lobby server
  pygame_game/
    settings.py            # Game settings and constants
    entities.py            # Character classes and ability logic
    __init__.py            # Package exports
    assets/
      tommy-background.png # Background image
      tommy-warrior.png    # Warrior character static image
      warrior-idle.gif     # Warrior character animated GIF
      Mage-idle.gif        # Mage character animated GIF
      Ghost-idle.gif       # Ghost character animated GIF
      ghost-confusion.gif  # Ghost confusion animation for extra turns
      titlescreen.jpg      # Title screen background
  README.md
  MULTIPLAYER_README.md    # Detailed multiplayer setup guide
```

## How to Run

### Single Player Mode
1. Open a terminal in the `Game` directory.
2. Install required packages:
   ```sh
   pip install pygame pillow
   ```
3. Run the game:
   ```sh
   python main.py
   ```
4. The game will launch with a title screen. Use **W/S** or **Up/Down** to navigate and **Enter** to select.

### Multiplayer Mode
1. **Start the Lobby Server** (required for multiplayer):
   ```sh
   python lobby_server.py
   ```
2. **Run the game** in a separate terminal:
   ```sh
   python main.py
   ```
3. Select **"Play with Others"** from the title screen
4. Choose to create or join a lobby
5. **Character Selection**: Both players choose their characters and names
6. **Game Start**: Automatic synchronization when both players are ready

## Game Modes

### Single Player (Local)
- Two players on the same computer
- Turn-based combat with keyboard controls
- Character selection for both players
- No network required

### Multiplayer (Online)
- Play with friends over the internet
- Create or join lobbies with 4-digit codes
- **Synchronized character selection** - no duplicate classes
- Real-time game synchronization
- Cross-platform compatibility

## Title Screen

The game starts with a beautiful title screen featuring:
- **Play!**: Start a local two-player game
- **Play with Others**: Access multiplayer features with character selection
- **Settings**: Configure game options
- **Exit**: Quit the game

## Gameplay

### Character Selection
- Choose between **Warrior**, **Mage**, and **Ghost** for each player
- Customize character names
- Each class has unique abilities, stats, and visual effects
- Animated GIF sprites for all character classes
- **Multiplayer**: Real-time synchronization prevents duplicate class choices

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
  - **Health Potion (R/P):** Restore 30 HP (limited to 2 uses per character)
- **Special:** Animated GIF sprite

#### Mage
- **Health:** 80 HP
- **Abilities:**
  - **Light Attack (Q/U):** Quick, reliable attack (10-14 damage)
  - **Fireball (W/I):** Fiery magical attack with 25% chance to poison (20-25 damage, poison deals 1-5 damage per turn for 3 turns)
  - **Heal (E/O):** Restore 25 HP to yourself (limited to 2 uses per character)
  - **Health Potion (R/P):** Restore 30 HP (limited to 2 uses per character)
- **Special:** Animated GIF sprite

#### Ghost
- **Health:** 100 HP
- **Abilities:**
  - **Light Attack (Q/U):** Quick, reliable attack (10-14 damage)
  - **Slash (W/I):** Powerful slash with 25% chance to cause bleeding (15-20 damage)
  - **Confusion (E/O):** Confusing attack that deals 10 damage with 20% chance to grant an extra turn
  - **Souls (R/P):** Steal the enemy's soul and heal yourself for 30 HP (limited to 2 uses per character)
- **Special:** Animated GIF sprite, unique extra turn mechanic, and special confusion animation when extra turn is granted

### Status Effects

- **Stunned:** Applied by Warrior's Heavy Strike. Target misses their next turn
- **Poisoned:** Applied by Mage's Fireball. Target takes 1-5 damage per turn for 3 turns
- **Bleeding:** Applied by Ghost's Slash. Target takes 1 damage per turn for 5 turns

### Dynamic UI

- Health bars, character names, and ability keys are displayed on the same side as each character
- UI automatically adjusts based on character positions
- Active player's abilities are highlighted in yellow
- Inactive player's abilities are shown in gray
- Health potion count is displayed next to the ability name (e.g., "R: Health Potion (2)")
- Healing ability uses are displayed next to the ability name (e.g., "E: Heal (2)")
- FPS counter displayed underneath the left health bar
- Turn indicator shows whose turn it is with colored borders around active player

## Multiplayer Features

### Lobby System
- **4-digit numeric codes** for easy sharing
- **Create Lobby**: Host a game and get a unique code
- **Join Lobby**: Enter a friend's code to join their game
- **Browse Lobbies**: See all available public lobbies
- **Real-time updates**: Instant notifications when players join/leave

### Character Selection in Multiplayer
- **Synchronized Selection**: Both players choose characters simultaneously
- **Class Filtering**: Automatically prevents duplicate class choices
- **Real-time Updates**: See when other player selects a class
- **Custom Names**: Each player can set their character name
- **Coordinated Start**: Game begins only when both players are ready

### Network Requirements
- **Local Network**: Works automatically on same WiFi/LAN
- **Internet Play**: Requires port forwarding (port 5555) or VPN service
- **Cross-Platform**: Works between Windows, Mac, and Linux

### Multiplayer Flow
1. **Host**: Start lobby server, create lobby, share 4-digit code
2. **Guest**: Enter code, join lobby
3. **Character Selection**: Both players choose classes and names
4. **Game**: Automatic synchronization of turns and actions

**📖 [Detailed Multiplayer Setup Guide](MULTIPLAYER_README.md)** - Complete instructions for multiplayer setup, troubleshooting, and advanced configuration.

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
- All character classes (Warrior, Mage, Ghost) use animated GIF sprites
- Smooth animation in both character selection and in-game
- Special confusion animation for Ghost's extra turn mechanic
- Uses Pillow library for GIF frame extraction
- Fallback to static images if GIFs are unavailable

### Advanced Ability System
- Status effects with duration tracking
- Extra turn mechanics (Ghost's Confusion)
- Blocking system to counter attacks (doesn't block healing abilities)
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
- Adaptive UI positioning for different screen sizes

### Multiplayer Architecture
- Client-server architecture for reliable connections
- JSON-based message protocol
- Automatic lobby cleanup and player management
- Socket timeout handling for stable connections
- **Character selection synchronization**
- **Real-time game state coordination**

## Customization
- Edit `pygame_game/settings.py` to change health, damage values, and other game settings
- Replace images in `pygame_game/assets/` to use your own characters or backgrounds
- Add animated GIFs for new character classes
- Modify `pygame_game/entities.py` to add new abilities or character classes
- Customize multiplayer settings in `multiplayer.py`

## Recent Updates & Bug Fixes

### Latest Improvements
- **Fixed Warrior Block Bug**: Warrior's block ability no longer blocks their own health potion
- **Improved Resolution Menu**: Instructions now properly positioned without overlapping resolution options
- **Enhanced Multiplayer**: Added synchronized character selection with real-time class filtering
- **Better UI Positioning**: Adaptive text positioning for different screen sizes and resolutions

## Troubleshooting

### General Issues
- If images do not show in the graphical game, check the file paths in `main.py` and ensure your images are in `pygame_game/assets/`
- If you see errors about missing modules, make sure you installed pygame and pillow:
  ```sh
  pip install pygame pillow
  ```
- For animated GIFs, ensure the Pillow library is installed for proper frame extraction
- If resolution changes don't apply, try restarting the game
- For performance issues, try lowering the resolution or FPS in the settings menu

### Multiplayer Issues
- **"Failed to connect to server"**: Make sure the lobby server is running (`python lobby_server.py`)
- **"Lobby not found"**: Check the 4-digit code is correct
- **Connection timeouts**: Check firewall settings and port forwarding
- **Can't join from different network**: Configure port forwarding on router (port 5555)
- **Server crashes**: Delete `__pycache__` folders and restart server
- **Character selection stuck**: Check if both players are connected and try refreshing

### Network Setup for Internet Play
1. Find your public IP address (whatismyipaddress.com)
2. Configure port forwarding on your router (port 5555)
3. Update client connection settings with your public IP
4. Ensure firewall allows connections on port 5555

---

## Creators

**Coder:** Louie Brooker  
Business email: brookerlouie7@gmail.com

**Artist:** Tommy Batchelor  
Business email: tommybatchelor986@gmail.com

Enjoy your turn-based battle! For multiplayer help, see `MULTIPLAYER_README.md` or check the troubleshooting section. 