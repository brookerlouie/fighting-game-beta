# LEGACY FILE: See terminal_game/settings.py and terminal_game/main.py for the current text-based game logic.
# This file is no longer used in the refactored project structure.

# settings.py
# Game configuration and settings

# Game balance settings
DEFAULT_WARRIOR_HEALTH = 120
DEFAULT_MAGE_HEALTH = 80
HEALTH_POTION_AMOUNT = 30
HEAVY_STRIKE_MIN = 5
HEAVY_STRIKE_MAX = 15
FIREBALL_MIN = 10
FIREBALL_MAX = 20
POISON_DAMAGE = 5
POISON_DURATION = 3
HEAL_AMOUNT = 25

# Display settings
WIDTH = 800
HEIGHT = 600
FPS = 60

# Resolution options (width, height, fps)
RESOLUTION_OPTIONS = [
    (1920, 1080, 60),  # Default for your laptop
    (800, 600, 60),
    (1024, 768, 60),
    (1280, 720, 60),
    (1280, 720, 120),
    (1920, 1080, 120),
    (1920, 1080, 144)
]

# Current settings (will be modified by settings menu)
CURRENT_RESOLUTION_INDEX = 0  # Index in RESOLUTION_OPTIONS - now defaults to 1920x1080 @ 60fps
BRIGHTNESS = 100  # 0-150 range
FULLSCREEN = True  # Start in fullscreen mode

# Game settings
PLAYER_SPEED = 5
PLAYER_SIZE = 50
BACKGROUND_COLOR = (30, 30, 30)

def get_current_resolution():
    """Get the current resolution and FPS settings"""
    return RESOLUTION_OPTIONS[CURRENT_RESOLUTION_INDEX]

def get_brightness_multiplier():
    """Get brightness multiplier (0.0 to 1.5)"""
    return BRIGHTNESS / 100.0

def apply_brightness_to_color(color):
    """Apply brightness setting to a color tuple"""
    multiplier = get_brightness_multiplier()
    return tuple(min(255, int(c * multiplier)) for c in color)
