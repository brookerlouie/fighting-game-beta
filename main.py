# LEGACY FILE: The main pygame game is now in pygame_game/main.py. This file is no longer used in the refactored project structure.

# main.py
# Entry point for your game

# Import your game modules here
# from game.engine import GameEngine

import pygame
import sys
import math
import pygame_game.settings as settings
from pygame_game.settings import get_current_resolution, apply_brightness_to_color, RESOLUTION_OPTIONS, BRIGHTNESS, FULLSCREEN
from pygame_game.entities import create_warrior, create_mage, create_ghost
from PIL import Image
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'pygame_game', 'assets')

def is_in_range(player1, player2, max_distance):
    dx = player1.x - player2.x
    dy = player1.y - player2.y
    distance = math.hypot(dx, dy)
    return distance <= max_distance


pygame.init()
# Get the user's current screen size for fullscreen
info = pygame.display.Info()
# Use the current resolution from settings
WIDTH, HEIGHT, FPS = get_current_resolution()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Fighting Game")
clock = pygame.time.Clock()

# Load and scale background image to always fill the screen
try:
    background_path = os.path.join(ASSETS_DIR, 'tommy-background.png')
    background = pygame.image.load(background_path)
    background = background.convert()
    original_size = background.get_size()
    print(f"Background loaded successfully. Original size: {original_size}")
    print(f"Screen size: {WIDTH}x{HEIGHT}")
    
    # Better scaling for small images - scale up first, then down for better quality
    if original_size[0] < WIDTH or original_size[1] < HEIGHT:
        print("Small image detected - using high-quality scaling...")
        # Scale up to 2x the target size first for better quality
        temp_width = WIDTH * 2
        temp_height = HEIGHT * 2
        background = pygame.transform.smoothscale(background, (temp_width, temp_height))
        # Then scale down to final size
        background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))
    else:
        # Direct scale down for large images
        background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))
    
    print(f"Background scaled to: {background.get_width()}x{background.get_height()}")
    
except Exception as e:
    print("Failed to load background image:", e)
    print("Trying fallback background...")
    background = None
    
# Utility to load animated GIF frames as pygame surfaces
def load_gif_frames(path, size):
    frames = []
    try:
        img = Image.open(path)
        n_frames = getattr(img, 'n_frames', 1)
        print(f"Loading GIF {path}: {n_frames} frames, target size: {size}")
        
        for frame in range(n_frames):
            img.seek(frame)
            # Convert to RGBA and resize to target size
            frame_img = img.convert('RGBA').resize(size, Image.Resampling.LANCZOS)
            # Convert to pygame surface
            data = frame_img.tobytes()
            surface = pygame.image.fromstring(data, frame_img.size, 'RGBA')
            frames.append(surface)
        
        print(f"Successfully loaded {len(frames)} frames, first frame size: {frames[0].get_size() if frames else 'None'}")
    except Exception as e:
        print(f"Failed to load GIF {path}: {e}")
    return frames

CHAR_SIZE = 500  # Set this at the top
# Load and scale player images (optional) using relative paths
try:
    warrior_path = os.path.join(ASSETS_DIR, 'tommy-warrior.png')
    warrior_img = pygame.image.load(warrior_path)
    warrior_img = pygame.transform.scale(warrior_img, (CHAR_SIZE, CHAR_SIZE))
except Exception as e:
    print("Failed to load warrior image:", e)
    warrior_img = None

# Load warrior animated GIF for in-game use
try:
    warrior_gif_path = os.path.join(ASSETS_DIR, 'warrior-idle.gif')
    warrior_gif_frames = load_gif_frames(warrior_gif_path, (CHAR_SIZE, CHAR_SIZE))
    warrior_gif_img = warrior_gif_frames[0] if warrior_gif_frames else None
except Exception as e:
    print("Failed to load warrior gif:", e)
    warrior_gif_frames = []
    warrior_gif_img = None

# Load ghost confusion animation
try:
    ghost_confusion_path = os.path.join(ASSETS_DIR, 'ghost-confusion.gif')
    ghost_confusion_frames = load_gif_frames(ghost_confusion_path, (CHAR_SIZE, CHAR_SIZE))
    ghost_confusion_img = ghost_confusion_frames[0] if ghost_confusion_frames else None
    print(f"Ghost confusion animation loaded: {len(ghost_confusion_frames)} frames")
except Exception as e:
    print("Failed to load ghost confusion gif:", e)
    ghost_confusion_frames = []
    ghost_confusion_img = None

try:
    mage_gif_path = os.path.join(ASSETS_DIR, 'Mage-idle.gif')
    mage_gif_frames = load_gif_frames(mage_gif_path, (CHAR_SIZE, CHAR_SIZE))
    mage_img = mage_gif_frames[0] if mage_gif_frames else None
except Exception as e:
    print("Failed to load mage gif:", e)
    mage_gif_frames = []
    mage_img = None
try:
    ghost_gif_path = os.path.join(ASSETS_DIR, 'Ghost-idle.gif')
    ghost_gif_frames = load_gif_frames(ghost_gif_path, (CHAR_SIZE, CHAR_SIZE))
    ghost_img = ghost_gif_frames[0] if ghost_gif_frames else None
except Exception as e:
    print("Failed to load ghost gif:", e)
    ghost_gif_frames = []
    ghost_img = None

font = pygame.font.SysFont(None, 64)
small_font = pygame.font.SysFont(None, 36)
name_font = pygame.font.SysFont(None, 48)

def draw_health_bar(surface, x, y, current_health, max_health, width=50, height=8):
    pygame.draw.rect(surface, (60, 60, 60), (x, y, width, height))
    health_width = int(width * (current_health / max_health))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, health_width, height))
    pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 2)

ability_font = pygame.font.SysFont(None, 32)
padding = 10
ability_y = HEIGHT - 120

# Add turn variable for turn-based gameplay
turn = 1  # 1 for Player 1, 2 for Player 2

# Define ability keys by player number
player1_keys = ["Q", "W", "E", "R"]
player2_keys = ["U", "I", "O", "P"]

# Add game over state
game_over = False
winner = None
paused = False  # Pause menu state

# Animation state
warrior_anim_index = 0
warrior_anim_timer = 0
warrior_anim_speed = 6  # frames per second

mage_anim_index = 0
mage_anim_timer = 0
mage_anim_speed = 6  # frames per second

ghost_anim_index = 0
ghost_anim_timer = 0
ghost_anim_speed = 6  # frames per second

ghost_confusion_anim_index = 0
ghost_confusion_anim_timer = 0
ghost_confusion_anim_speed = 6  # frames per second
ghost_confusion_active = False  # Track if confusion animation is playing
ghost_confusion_duration = 0  # How long to show confusion animation

def character_selection(player_num, available_classes=None):
    classes = available_classes if available_classes else ["Warrior", "Mage", "Ghost"]
    selected = 0
    name = ""
    input_active = False
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not input_active:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        selected = (selected - 1) % len(classes)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        selected = (selected + 1) % len(classes)
                    elif event.key == pygame.K_RETURN:
                        input_active = True
                else:
                    if event.key == pygame.K_RETURN:
                        if name.strip() == "":
                            name = classes[selected]
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 12 and event.unicode.isprintable():
                            name += event.unicode

        # Draw selection screen
        screen.fill((20, 20, 40))
        title = font.render(f"Player {player_num}: Choose your class", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        positions = [int((WIDTH * (j + 1)) / (len(classes) + 1)) for j in range(len(classes))]
        for i, cls in enumerate(classes):
            x_pos = positions[i]
            color = (255, 255, 0) if i == selected else (200, 200, 200)
            txt = font.render(cls, True, color)
            screen.blit(txt, (x_pos - txt.get_width() // 2, 200))
            if cls == "Warrior" and "warrior_img" in globals() and warrior_img:
                screen.blit(warrior_img, (x_pos - warrior_img.get_width() // 2, 260))
            elif cls == "Mage" and mage_gif_frames:
                screen.blit(mage_gif_frames[mage_anim_index], (x_pos - mage_gif_frames[0].get_width() // 2, 260))
            elif cls == "Ghost" and ghost_gif_frames:
                screen.blit(ghost_gif_frames[ghost_anim_index], (x_pos - ghost_gif_frames[0].get_width() // 2, 260))

        if input_active:
            prompt_y = 260 + (warrior_img.get_height() if warrior_img else 150) + 20
            prompt = small_font.render("Enter your name (press Enter to confirm):", True, (255, 255, 255))
            screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, prompt_y))
            name_surface = font.render(name + "|", True, (0, 255, 0))
            screen.blit(name_surface, (WIDTH // 2 - name_surface.get_width() // 2, prompt_y + 40))

        pygame.display.flip()
        clock.tick(30)

    return classes[selected].lower(), name.strip() if name.strip() else classes[selected]

def settings_menu(screen, clock):
    global WIDTH, HEIGHT, FPS, BRIGHTNESS, CURRENT_RESOLUTION_INDEX
    global background
    """Settings menu with brightness, resolution, and FPS options"""
    
    selected_option = 0
    options = ["Brightness", "Resolution", "Back"]
    done = False
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Brightness
                        brightness_menu(screen, clock)
                    elif selected_option == 1:  # Resolution
                        screen = resolution_menu(screen, clock)
                    elif selected_option == 2:  # Back
                        done = True
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if selected_option == 0:  # Brightness
                        BRIGHTNESS = max(0, BRIGHTNESS - 10)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if selected_option == 0:  # Brightness
                        BRIGHTNESS = min(150, BRIGHTNESS + 10)
        
        # Draw settings menu
        screen.fill((20, 20, 40))
        
        title_font = pygame.font.SysFont(None, 72)
        title = title_font.render("SETTINGS", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        
        option_font = pygame.font.SysFont(None, 48)
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected_option else (200, 200, 200)
            text = option
            
            # Add current values
            if option == "Brightness":
                text += f": {BRIGHTNESS}%"
            elif option == "Resolution":
                current_res = get_current_resolution()
                text += f": {current_res[0]}x{current_res[1]} @ {current_res[2]}fps"
            
            option_surface = option_font.render(text, True, color)
            y_pos = 250 + i * 60
            screen.blit(option_surface, (WIDTH // 2 - option_surface.get_width() // 2, y_pos))
        
        # Instructions
        instruction_font = pygame.font.SysFont(None, 32)
        instructions = [
            "Use W/S or Up/Down to navigate",
            "Use A/D or Left/Right to adjust values",
            "Press Enter to select, ESC to go back"
        ]
        for i, instruction in enumerate(instructions):
            instruction_surface = instruction_font.render(instruction, True, (150, 150, 150))
            screen.blit(instruction_surface, (WIDTH // 2 - instruction_surface.get_width() // 2, 500 + i * 30))
        
        pygame.display.flip()
        clock.tick(30)
    
    return screen

def brightness_menu(screen, clock):
    global BRIGHTNESS
    """Brightness adjustment menu"""
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    BRIGHTNESS = max(0, BRIGHTNESS - 5)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    BRIGHTNESS = min(150, BRIGHTNESS + 5)
        
        # Draw brightness menu
        screen.fill((20, 20, 40))
        
        title_font = pygame.font.SysFont(None, 72)
        title = title_font.render("BRIGHTNESS", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        
        # Brightness bar
        bar_width = 400
        bar_height = 40
        bar_x = WIDTH // 2 - bar_width // 2
        bar_y = HEIGHT // 2 - 50
        
        # Background bar
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        
        # Brightness level
        brightness_width = int((BRIGHTNESS / 150.0) * bar_width)
        brightness_color = apply_brightness_to_color((255, 255, 255))
        pygame.draw.rect(screen, brightness_color, (bar_x, bar_y, brightness_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 3)
        
        # Brightness text
        value_font = pygame.font.SysFont(None, 48)
        value_text = f"{BRIGHTNESS}%"
        value_surface = value_font.render(value_text, True, (255, 255, 255))
        screen.blit(value_surface, (WIDTH // 2 - value_surface.get_width() // 2, bar_y + bar_height + 20))
        
        # Instructions
        instruction_font = pygame.font.SysFont(None, 32)
        instructions = [
            "Use A/D or Left/Right to adjust brightness",
            "Press ESC to go back"
        ]
        for i, instruction in enumerate(instructions):
            instruction_surface = instruction_font.render(instruction, True, (150, 150, 150))
            screen.blit(instruction_surface, (WIDTH // 2 - instruction_surface.get_width() // 2, 500 + i * 30))
        
        pygame.display.flip()
        clock.tick(30)

def resolution_menu(screen, clock):
    global WIDTH, HEIGHT, FPS
    global background
    """Resolution and FPS selection menu"""
    
    selected_resolution = settings.CURRENT_RESOLUTION_INDEX
    done = False
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected_resolution = (selected_resolution - 1) % len(RESOLUTION_OPTIONS)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected_resolution = (selected_resolution + 1) % len(RESOLUTION_OPTIONS)
                elif event.key == pygame.K_RETURN:
                    # Update the current resolution index first
                    settings.CURRENT_RESOLUTION_INDEX = selected_resolution
                    # Get the new resolution values
                    new_width, new_height, new_fps = RESOLUTION_OPTIONS[selected_resolution]
                    print(f"Changing resolution from {WIDTH}x{HEIGHT} @ {FPS}fps to {new_width}x{new_height} @ {new_fps}fps")
                    
                    # Update global variables
                    WIDTH, HEIGHT, FPS = new_width, new_height, new_fps
                    
                    screen = apply_display_settings(screen)
                    # Reposition players and UI after resolution/fullscreen change
                    player1.x = WIDTH // 4 - CHAR_SIZE // 2
                    player1.y = HEIGHT // 2 - CHAR_SIZE // 2 + OFFSET_Y
                    player2.x = 3 * WIDTH // 4 - CHAR_SIZE // 2
                    player2.y = HEIGHT // 2 - CHAR_SIZE // 2 + OFFSET_Y
                    global ability_y
                    ability_y = HEIGHT - 120
                    # Rescale background if needed
                    if background:
                        try:
                            original_size = background.get_size()
                            if original_size != (WIDTH, HEIGHT):
                                background = pygame.transform.smoothscale(background, (WIDTH, HEIGHT))
                        except Exception:
                            pass
                    print(f"Resolution changed successfully to {WIDTH}x{HEIGHT} @ {FPS}fps")
                    done = True
        
        # Draw resolution menu
        screen.fill((20, 20, 40))
        
        title_font = pygame.font.SysFont(None, 72)
        title = title_font.render("RESOLUTION & FPS", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        
        option_font = pygame.font.SysFont(None, 48)
        for i, (width, height, fps) in enumerate(RESOLUTION_OPTIONS):
            color = (255, 255, 0) if i == selected_resolution else (200, 200, 200)
            text = f"{width}x{height} @ {fps}fps"
            # Check if this resolution matches the current WIDTH, HEIGHT, FPS
            if width == WIDTH and height == HEIGHT and fps == FPS:
                text += " (Current)"
            
            option_surface = option_font.render(text, True, color)
            y_pos = 250 + i * 50
            screen.blit(option_surface, (WIDTH // 2 - option_surface.get_width() // 2, y_pos))
        
        # Instructions
        instruction_font = pygame.font.SysFont(None, 32)
        instructions = [
            "Use W/S or Up/Down to navigate",
            "Press Enter to apply, ESC to go back"
        ]
        for i, instruction in enumerate(instructions):
            instruction_surface = instruction_font.render(instruction, True, (150, 150, 150))
            screen.blit(instruction_surface, (WIDTH // 2 - instruction_surface.get_width() // 2, 500 + i * 30))
        
        pygame.display.flip()
        clock.tick(30)

    return screen

def apply_display_settings(screen):
    """Apply current display settings"""
    global WIDTH, HEIGHT, FPS
    
    # WIDTH, HEIGHT, FPS are already set by the calling function
    # Just apply the display mode with current values
    
    # Preserve fullscreen state when changing resolution
    if FULLSCREEN:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    pygame.display.set_caption("Fighting Game")
    return screen

# --- Character selection for both players ---
player1_class, player1_name = character_selection(1)
remaining_classes = [cls for cls in ["Warrior", "Mage", "Ghost"] if cls.lower() != player1_class.lower()]
player2_class, player2_name = character_selection(2, available_classes=remaining_classes)

OFFSET_Y = -40  # Negative value moves characters up

# --- Create players based on selection ---
if player1_class == "warrior":
    player1 = create_warrior()
elif player1_class == "mage":
    player1 = create_mage()
else:
    player1 = create_ghost()
player1.name = player1_name
player1.x = WIDTH // 4 - CHAR_SIZE // 2
player1.y = HEIGHT // 2 - CHAR_SIZE // 2 + OFFSET_Y

if player2_class == "warrior":
    player2 = create_warrior()
elif player2_class == "mage":
    player2 = create_mage()
else:
    player2 = create_ghost()
player2.name = player2_name
player2.x = 3 * WIDTH // 4 - CHAR_SIZE // 2
player2.y = HEIGHT // 2 - CHAR_SIZE // 2 + OFFSET_Y

ability_message = ""
message_timer = 0

# FPS tracking
fps_counter = 0
fps_timer = 0
current_fps = 0

running = True
while running:
    dt = clock.tick(FPS)  # milliseconds since last frame
    
    # Update FPS counter
    fps_counter += 1
    fps_timer += dt
    if fps_timer >= 1000:  # Update FPS every second
        current_fps = fps_counter
        fps_counter = 0
        fps_timer = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if paused and not game_over:
                mouse_pos = pygame.mouse.get_pos()
                # Check if Settings was clicked
                settings_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
                if settings_rect.collidepoint(mouse_pos):
                    screen = settings_menu(screen, clock)
                # Check if Exit Game was clicked
                exit_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 50)
                if exit_rect.collidepoint(mouse_pos):
                    running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not game_over:
                    paused = not paused  # Toggle pause menu
                else:
                    running = False  # Exit if game is over
            
            # Only allow ability usage if game is not over and not paused
            if not game_over and not paused:
                # Player 1's turn
                if turn == 1:
                    if event.key == pygame.K_q:
                        result = player1.use_ability(0, player2)
                        ability_message = result
                        message_timer = 120
                        turn = 2  # Switch to Player 2's turn
                    if event.key == pygame.K_w:
                        result = player1.use_ability(1, player2)
                        ability_message = result
                        message_timer = 120
                        turn = 2  # Switch to Player 2's turn
                    if event.key == pygame.K_e:
                        # For Ghost, Confusion targets enemy; for others, ability targets self
                        if player1_class == "ghost":
                            result = player1.use_ability(2, player2)
                        else:
                            result = player1.use_ability(2, player1)
                        ability_message = result
                        message_timer = 120
                        # Only switch turns if player doesn't get an extra turn
                        if not player1.extra_turn:
                            turn = 2  # Switch to Player 2's turn
                        else:
                            player1.extra_turn = False  # Reset the flag
                    if event.key == pygame.K_r:
                        print(f"R key pressed! Player 1 has {len(player1.abilities)} abilities")
                        print(f"Trying to use ability index 3...")
                        result = player1.use_ability(3, player1)
                        print(f"Result: {result}")
                        ability_message = result
                        message_timer = 120
                        turn = 2  # Switch to Player 2's turn

                # Player 2's turn
                if turn == 2:
                    if event.key == pygame.K_u:
                        result = player2.use_ability(0, player1)
                        ability_message = result
                        message_timer = 120
                        turn = 1  # Switch to Player 1's turn
                    if event.key == pygame.K_i:
                        result = player2.use_ability(1, player1)
                        ability_message = result
                        message_timer = 120
                        turn = 1  # Switch to Player 1's turn
                    if event.key == pygame.K_o:
                        # For Ghost, Confusion targets enemy; for others, ability targets self
                        if player2_class == "ghost":
                            result = player2.use_ability(2, player1)
                        else:
                            result = player2.use_ability(2, player2)
                        ability_message = result
                        message_timer = 120
                        # Only switch turns if player doesn't get an extra turn
                        if not player2.extra_turn:
                            turn = 1  # Switch to Player 1's turn
                        else:
                            player2.extra_turn = False  # Reset the flag
                    if event.key == pygame.K_p:
                        result = player2.use_ability(3, player2)
                        ability_message = result
                        message_timer = 120
                        turn = 1  # Switch to Player 1's turn

    # Check for game over conditions
    if not game_over:
        if player1.health <= 0:
            game_over = True
            winner = player2
        elif player2.health <= 0:
            game_over = True
            winner = player1

    # Check for confusion animation triggers
    if player1.confusion_animation_triggered:
        ghost_confusion_active = True
        ghost_confusion_duration = 2000  # Show for 2 seconds
        player1.confusion_animation_triggered = False
    elif player2.confusion_animation_triggered:
        ghost_confusion_active = True
        ghost_confusion_duration = 2000  # Show for 2 seconds
        player2.confusion_animation_triggered = False

    # Draw background - ensure it completely fills the screen
    if background:
        # Clear screen first to prevent any bleed-through
        screen.fill((0, 0, 0))
        # Fill the entire screen with the background
        screen.blit(background, (0, 0))
        # --- Apply brightness overlay ---
        if BRIGHTNESS != 100:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            if BRIGHTNESS < 100:
                # Darken: overlay black, max alpha 200 at 0%
                alpha = int(200 * (1 - BRIGHTNESS / 100))
                overlay.fill((0, 0, 0, alpha))
            else:
                # Brighten: overlay white, max alpha 100 at 150%
                alpha = int(100 * ((BRIGHTNESS - 100) / 50))  # 150% = max white overlay
                overlay.fill((255, 255, 255, min(alpha, 100)))
            screen.blit(overlay, (0, 0))
    else:
        # Fallback: solid color background with brightness applied
        bg_color = apply_brightness_to_color((30, 30, 30))
        screen.fill(bg_color)

    # --- Dynamic UI: Health bar, name, and abilities on the same side as the character ---

    # Helper to determine left/right
    def is_left(player):
        return player.x < WIDTH // 2

    # --- UI for Player 1 ---
    if is_left(player1):
        # Top left
        name_surface = name_font.render(player1.name, True, (255, 255, 0) if player1_class == "warrior" else (0, 255, 255))
        screen.blit(name_surface, (20, 20))
        bar_x, bar_y, bar_w, bar_h = 20, 70, 400, 40
        draw_health_bar(screen, bar_x, bar_y, player1.health, player1.max_health, width=bar_w, height=bar_h)
        health_text = f"{player1.health} / {player1.max_health}"
        health_surface = name_font.render(health_text, True, (255, 255, 255))
        screen.blit(health_surface, (bar_x + bar_w // 2 - health_surface.get_width() // 2, bar_y + bar_h // 2 - health_surface.get_height() // 2))
        
        # FPS counter underneath left health bar
        fps_font = pygame.font.SysFont(None, 20)  # Small font
        fps_text = f"FPS: {current_fps}"
        fps_surface = fps_font.render(fps_text, True, (150, 150, 150))  # Gray color
        screen.blit(fps_surface, (bar_x, bar_y + bar_h + 5))  # 5 pixels below health bar
        
        # Abilities bottom left
        for i, ability in enumerate(player1.abilities):
            key = player1_keys[i]
            text = f"{key}: {ability.name}"
            # Add potion count for Health Potion ability
            if ability.name == "Health Potion":
                text += f" ({player1.health_potions})"
            # Add healing uses count for healing abilities
            elif ability.name in ["Heal", "Souls"]:
                text += f" ({player1.healing_uses})"
            color = (255, 255, 0) if (player1_class == "warrior" and turn == 1) or (player1_class == "mage" and turn == 1) else (180, 180, 180)
            surf = ability_font.render(text, True, color)
            screen.blit(surf, (padding, ability_y + i * 32))
    else:
        # Top right
        name_surface = name_font.render(player1.name, True, (255, 255, 0) if player1_class == "warrior" else (0, 255, 255))
        screen.blit(name_surface, (WIDTH - name_surface.get_width() - 20, 20))
        bar_x, bar_y, bar_w, bar_h = WIDTH - 420, 70, 400, 40
        draw_health_bar(screen, bar_x, bar_y, player1.health, player1.max_health, width=bar_w, height=bar_h)
        health_text = f"{player1.health} / {player1.max_health}"
        health_surface = name_font.render(health_text, True, (255, 255, 255))
        screen.blit(health_surface, (bar_x + bar_w // 2 - health_surface.get_width() // 2, bar_y + bar_h // 2 - health_surface.get_height() // 2))
        # Abilities bottom right
        for i, ability in enumerate(player1.abilities):
            key = player1_keys[i]
            text = f"{key}: {ability.name}"
            # Add potion count for Health Potion ability
            if ability.name == "Health Potion":
                text += f" ({player1.health_potions})"
            # Add healing uses count for healing abilities
            elif ability.name in ["Heal", "Souls"]:
                text += f" ({player1.healing_uses})"
            color = (255, 255, 0) if (player1_class == "warrior" and turn == 1) or (player1_class == "mage" and turn == 1) else (180, 180, 180)
            surf = ability_font.render(text, True, color)
            screen.blit(surf, (WIDTH - surf.get_width() - padding, ability_y + i * 32))

    # --- UI for Player 2 ---
    if is_left(player2):
        # Top left
        name_surface = name_font.render(player2.name, True, (255, 255, 0) if player2_class == "warrior" else (0, 255, 255))
        screen.blit(name_surface, (20, 20))
        bar_x, bar_y, bar_w, bar_h = 20, 70, 400, 40
        draw_health_bar(screen, bar_x, bar_y, player2.health, player2.max_health, width=bar_w, height=bar_h)
        health_text = f"{player2.health} / {player2.max_health}"
        health_surface = name_font.render(health_text, True, (255, 255, 255))
        screen.blit(health_surface, (bar_x + bar_w // 2 - health_surface.get_width() // 2, bar_y + bar_h // 2 - health_surface.get_height() // 2))
        
        # FPS counter underneath left health bar (for Player 2 when on left)
        fps_font = pygame.font.SysFont(None, 20)  # Small font
        fps_text = f"FPS: {current_fps}"
        fps_surface = fps_font.render(fps_text, True, (150, 150, 150))  # Gray color
        screen.blit(fps_surface, (bar_x, bar_y + bar_h + 5))  # 5 pixels below health bar
        
        # Abilities bottom left
        for i, ability in enumerate(player2.abilities):
            key = player2_keys[i]
            text = f"{key}: {ability.name}"
            # Add potion count for Health Potion ability
            if ability.name == "Health Potion":
                text += f" ({player2.health_potions})"
            # Add healing uses count for healing abilities
            elif ability.name in ["Heal", "Souls"]:
                text += f" ({player2.healing_uses})"
            color = (255, 255, 0) if (player2_class == "warrior" and turn == 2) or (player2_class == "mage" and turn == 2) else (180, 180, 180)
            surf = ability_font.render(text, True, color)
            screen.blit(surf, (padding, ability_y + i * 32))
    else:
        # Top right
        name_surface = name_font.render(player2.name, True, (255, 255, 0) if player2_class == "warrior" else (0, 255, 255))
        screen.blit(name_surface, (WIDTH - name_surface.get_width() - 20, 20))
        bar_x, bar_y, bar_w, bar_h = WIDTH - 420, 70, 400, 40
        draw_health_bar(screen, bar_x, bar_y, player2.health, player2.max_health, width=bar_w, height=bar_h)
        health_text = f"{player2.health} / {player2.max_health}"
        health_surface = name_font.render(health_text, True, (255, 255, 255))
        screen.blit(health_surface, (bar_x + bar_w // 2 - health_surface.get_width() // 2, bar_y + bar_h // 2 - health_surface.get_height() // 2))
        # Abilities bottom right
        for i, ability in enumerate(player2.abilities):
            key = player2_keys[i]
            text = f"{key}: {ability.name}"
            # Add potion count for Health Potion ability
            if ability.name == "Health Potion":
                text += f" ({player2.health_potions})"
            # Add healing uses count for healing abilities
            elif ability.name in ["Heal", "Souls"]:
                text += f" ({player2.healing_uses})"
            color = (255, 255, 0) if (player2_class == "warrior" and turn == 2) or (player2_class == "mage" and turn == 2) else (180, 180, 180)
            surf = ability_font.render(text, True, color)
            screen.blit(surf, (WIDTH - surf.get_width() - padding, ability_y + i * 32))

    # Draw player 1
    if player1_class == "ghost" and ghost_confusion_active and ghost_confusion_frames:
        confusion_surface = ghost_confusion_frames[ghost_confusion_anim_index]
        # Center the confusion animation on the character position
        confusion_x = player1.x + (CHAR_SIZE - confusion_surface.get_width()) // 2
        confusion_y = player1.y + (CHAR_SIZE - confusion_surface.get_height()) // 2
        screen.blit(confusion_surface, (confusion_x, confusion_y))
        # Debug: print size when confusion animation is active
        if ghost_confusion_duration > 1900:  # Only print once at start
            print(f"Drawing confusion animation: size {confusion_surface.get_size()}, centered at ({confusion_x}, {confusion_y})")
    elif player1_class == "warrior" and warrior_gif_frames:
        screen.blit(warrior_gif_frames[warrior_anim_index], (player1.x, player1.y))
    elif player1_class == "mage" and mage_gif_frames:
        screen.blit(mage_gif_frames[mage_anim_index], (player1.x, player1.y))
    elif player1_class == "ghost" and ghost_gif_frames:
        screen.blit(ghost_gif_frames[ghost_anim_index], (player1.x, player1.y))
    else:
        pygame.draw.rect(screen, (255, 0, 0), (player1.x, player1.y, CHAR_SIZE, CHAR_SIZE))

    # Draw player 2
    if player2_class == "ghost" and ghost_confusion_active and ghost_confusion_frames:
        confusion_surface = ghost_confusion_frames[ghost_confusion_anim_index]
        # Center the confusion animation on the character position
        confusion_x = player2.x + (CHAR_SIZE - confusion_surface.get_width()) // 2
        confusion_y = player2.y + (CHAR_SIZE - confusion_surface.get_height()) // 2
        screen.blit(confusion_surface, (confusion_x, confusion_y))
        # Debug: print size when confusion animation is active
        if ghost_confusion_duration > 1900:  # Only print once at start
            print(f"Drawing confusion animation: size {confusion_surface.get_size()}, centered at ({confusion_x}, {confusion_y})")
    elif player2_class == "warrior" and warrior_gif_frames:
        screen.blit(warrior_gif_frames[warrior_anim_index], (player2.x, player2.y))
    elif player2_class == "mage" and mage_gif_frames:
        screen.blit(mage_gif_frames[mage_anim_index], (player2.x, player2.y))
    elif player2_class == "ghost" and ghost_gif_frames:
        screen.blit(ghost_gif_frames[ghost_anim_index], (player2.x, player2.y))
    else:
        pygame.draw.rect(screen, (0, 0, 255), (player2.x, player2.y, CHAR_SIZE, CHAR_SIZE))

    # Display game state
    if game_over and winner:
        # Victory screen
        victory_font = pygame.font.SysFont(None, 72)
        victory_msg = f"{winner.name} Wins!"
        victory_surface = victory_font.render(victory_msg, True, (255, 215, 0))  # Gold color
        screen.blit(victory_surface, (WIDTH // 2 - victory_surface.get_width() // 2, HEIGHT // 2 - 100))
        
        # Display winner's character image
        if winner == player1:
            if player1_class == "warrior" and warrior_gif_frames:
                winner_img = warrior_gif_frames[warrior_anim_index]
            elif player1_class == "mage" and mage_gif_frames:
                winner_img = mage_gif_frames[mage_anim_index]
            elif player1_class == "ghost" and ghost_gif_frames:
                winner_img = ghost_gif_frames[ghost_anim_index]
            else:
                winner_img = None
        else:  # winner == player2
            if player2_class == "warrior" and warrior_gif_frames:
                winner_img = warrior_gif_frames[warrior_anim_index]
            elif player2_class == "mage" and mage_gif_frames:
                winner_img = mage_gif_frames[mage_anim_index]
            elif player2_class == "ghost" and ghost_gif_frames:
                winner_img = ghost_gif_frames[ghost_anim_index]
            else:
                winner_img = None
        
        if winner_img:
            # Scale down the winner image for the victory screen
            winner_img_small = pygame.transform.scale(winner_img, (150, 150))
            screen.blit(winner_img_small, (WIDTH // 2 - 75, HEIGHT // 2 + 20))
        
        # Instructions to restart
        restart_font = pygame.font.SysFont(None, 36)
        restart_msg = "Press ESC to quit"
        restart_surface = restart_font.render(restart_msg, True, (255, 255, 255))
        screen.blit(restart_surface, (WIDTH // 2 - restart_surface.get_width() // 2, HEIGHT // 2 + 200))
        
    else:
        # Normal game display - show turn indicator
        # Display whose turn it is - make it very obvious!
        turn_font = pygame.font.SysFont(None, 48)
        turn_msg = f"Player {turn}'s Turn"
        turn_color = (255, 255, 0) if turn == 1 else (0, 255, 255)  # Yellow for P1, Cyan for P2
        turn_surface = turn_font.render(turn_msg, True, turn_color)
        screen.blit(turn_surface, (WIDTH // 2 - turn_surface.get_width() // 2, 30))

        # Add a visual indicator around the active player
        if turn == 1:
            # Highlight Player 1 with a colored border
            pygame.draw.rect(screen, (255, 255, 0), (player1.x - 5, player1.y - 5, CHAR_SIZE + 10, CHAR_SIZE + 10), 3)
        else:
            # Highlight Player 2 with a colored border
            pygame.draw.rect(screen, (0, 255, 255), (player2.x - 5, player2.y - 5, CHAR_SIZE + 10, CHAR_SIZE + 10), 3)

    if ability_message and message_timer > 0:
        msg_font = pygame.font.SysFont(None, 36)
        lines = ability_message.split('\n')
        for i, line in enumerate(lines):
            msg_surface = msg_font.render(line, True, (255, 255, 0))
            screen.blit(msg_surface, (WIDTH // 2 - msg_surface.get_width() // 2, HEIGHT - 100 + i * 30))
        message_timer -= 1
    else:
        ability_message = ""

    # Update animation timers
    if warrior_gif_frames:
        warrior_anim_timer += dt
        if warrior_anim_timer > 1000 // warrior_anim_speed:
            warrior_anim_index = (warrior_anim_index + 1) % len(warrior_gif_frames)
            warrior_anim_timer = 0
    if mage_gif_frames:
        mage_anim_timer += dt
        if mage_anim_timer > 1000 // mage_anim_speed:
            mage_anim_index = (mage_anim_index + 1) % len(mage_gif_frames)
            mage_anim_timer = 0
    if ghost_gif_frames:
        ghost_anim_timer += dt
        if ghost_anim_timer > 1000 // ghost_anim_speed:
            ghost_anim_index = (ghost_anim_index + 1) % len(ghost_gif_frames)
            ghost_anim_timer = 0
    
    # Update confusion animation
    if ghost_confusion_active and ghost_confusion_frames:
        ghost_confusion_anim_timer += dt
        if ghost_confusion_anim_timer > 1000 // ghost_confusion_anim_speed:
            ghost_confusion_anim_index = (ghost_confusion_anim_index + 1) % len(ghost_confusion_frames)
            ghost_confusion_anim_timer = 0
        
        # Check if confusion animation should end
        ghost_confusion_duration -= dt
        if ghost_confusion_duration <= 0:
            ghost_confusion_active = False
            ghost_confusion_anim_index = 0

    # Draw pause menu if game is paused
    if paused and not game_over:
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Pause menu
        pause_font = pygame.font.SysFont(None, 72)
        pause_title = pause_font.render("PAUSED", True, (255, 255, 255))
        screen.blit(pause_title, (WIDTH // 2 - pause_title.get_width() // 2, HEIGHT // 2 - 150))
        
        # Menu options
        menu_font = pygame.font.SysFont(None, 48)
        options = [
            ("Settings", (255, 255, 0)),
            ("Exit Game", (255, 100, 100))
        ]
        
        for i, (option, color) in enumerate(options):
            option_surface = menu_font.render(option, True, color)
            y_pos = HEIGHT // 2 - 50 + i * 60
            screen.blit(option_surface, (WIDTH // 2 - option_surface.get_width() // 2, y_pos))
        
        # Instructions
        instruction_font = pygame.font.SysFont(None, 32)
        instruction_text = "Press ESC to resume or click an option"
        instruction_surface = instruction_font.render(instruction_text, True, (200, 200, 200))
        screen.blit(instruction_surface, (WIDTH // 2 - instruction_surface.get_width() // 2, HEIGHT // 2 + 150))

    pygame.display.flip()

pygame.quit()
sys.exit()