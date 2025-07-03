# Fighting Game (Pygame)

A turn-based two-player fighting game built with Python and pygame. Players take turns using abilities to defeat their opponent in a strategic battle.

## Project Structure

```
Game/
  main.py                  # Entry point for the graphical game
  pygame_game/
    settings.py            # Game settings and constants
    entities.py            # Character classes and ability logic
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
4. The game will launch in fullscreen. Press **Escape** or close the window to quit.

## Gameplay

### Character Selection
- Choose between **Warrior** and **Mage** for each player
- Customize character names
- Each class has unique abilities and stats

### Turn-Based Combat
- Players take turns using abilities
- Only the active player can use their abilities
- After using an ability, the turn switches to the other player
- No movement - focus on strategic ability usage

### Controls

#### Player 1 (Left side)
- **Q**: Light Attack (damage ability)
- **E**: Heavy Strike (damage ability with stun chance)
- **R**: Block (blocks next attack)
- **F**: Health Potion (healing)

#### Player 2 (Right side)
- **Comma (,):** Light Attack (damage ability)
- **Period (.):** Fireball (damage ability with poison chance)
- **Quote ('):** Heal (self-healing)
- **Hash (#):** Health Potion (healing)

### Character Classes

#### Warrior
- Higher health (120 HP)
- **Abilities:** Light Attack, Heavy Strike, Block, Health Potion
- Heavy Strike has a chance to stun the opponent

#### Mage
- Lower health (80 HP) but powerful abilities
- **Abilities:** Light Attack, Fireball, Heal, Health Potion
- Fireball has a chance to poison the opponent

## Customization
- Edit `pygame_game/settings.py` to change health, damage values, and other game settings
- Replace images in `pygame_game/assets/` to use your own characters or backgrounds
- Modify `pygame_game/entities.py` to add new abilities or character classes

## Troubleshooting
- If images do not show in the graphical game, check the file paths in `main.py` and ensure your images are in `pygame_game/assets/`
- If you see errors about missing modules, make sure you installed pygame with `pip install pygame`

---

## Creators

**Coder:** Louie Brooker  
Business email: brookerlouie7@gmail.com

**Artist:** Tommy Batchelor  
Business email: tommybatchelor986@gmail.com

Enjoy your turn-based battle! If you have issues, check the troubleshooting section or ask for help. 