# LEGACY FILE: The main pygame game is now in pygame_game/main.py. This file is no longer used in the refactored project structure.

# main.py
# Entry point for your game

# Import your game modules here
# from game.engine import GameEngine

import pygame
import sys
import math
from pygame_game.settings import WIDTH, HEIGHT
from pygame_game.entities import create_warrior, create_mage

def is_in_range(player1, player2, max_distance):
    dx = player1.x - player2.x
    dy = player1.y - player2.y
    distance = math.hypot(dx, dy)
    return distance <= max_distance


pygame.init()
# Get the user's current screen size for fullscreen
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Fighting Game")
clock = pygame.time.Clock()

# Load and scale background image to always fill the screen
try:
    background = pygame.image.load(r"C:\Users\brook\OneDrive\Desktop\code\Game\pygame_game\assets\background4-1.png")
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
    
# Load and scale player images (optional) using absolute paths
CHAR_SIZE = 300  # Set this at the top
try:
    warrior_img = pygame.image.load(r"C:\Users\brook\OneDrive\Desktop\code\Game\pygame_game\assets\warrior.png")
    warrior_img = pygame.transform.scale(warrior_img, (CHAR_SIZE, CHAR_SIZE))
except Exception as e:
    print("Failed to load warrior image:", e)
    warrior_img = None
try:
    mage_img = pygame.image.load(r"C:\Users\brook\OneDrive\Desktop\code\Game\pygame_game\assets\mage.png")
    mage_img = pygame.transform.scale(mage_img, (CHAR_SIZE, CHAR_SIZE))
except Exception as e:
    print("Failed to load mage image:", e)
    mage_img = None

font = pygame.font.SysFont(None, 64)
small_font = pygame.font.SysFont(None, 36)

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

# Add game over state
game_over = False
winner = None

def character_selection(player_num, available_classes=None):
    classes = available_classes if available_classes else ["Warrior", "Mage"]
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

        positions = [WIDTH // 3, 2 * WIDTH // 3]
        for i, cls in enumerate(classes):
            x_pos = positions[i]
            color = (255, 255, 0) if i == selected else (200, 200, 200)
            txt = font.render(cls, True, color)
            screen.blit(txt, (x_pos - txt.get_width() // 2, 200))
            if cls == "Warrior" and "warrior_img" in globals() and warrior_img:
                screen.blit(warrior_img, (x_pos - warrior_img.get_width() // 2, 260))
            elif cls == "Mage" and "mage_img" in globals() and mage_img:
                screen.blit(mage_img, (x_pos - mage_img.get_width() // 2, 260))

        if input_active:
            prompt_y = 260 + (warrior_img.get_height() if warrior_img else 150) + 20
            prompt = small_font.render("Enter your name (press Enter to confirm):", True, (255, 255, 255))
            screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, prompt_y))
            name_surface = font.render(name + "|", True, (0, 255, 0))
            screen.blit(name_surface, (WIDTH // 2 - name_surface.get_width() // 2, prompt_y + 40))

        pygame.display.flip()
        clock.tick(30)

    return classes[selected].lower(), name.strip() if name.strip() else classes[selected]

# --- Character selection for both players ---
player1_class, player1_name = character_selection(1)
remaining_classes = [cls for cls in ["Warrior", "Mage"] if cls.lower() != player1_class.lower()]
player2_class, player2_name = character_selection(2, available_classes=remaining_classes)

# --- Create players based on selection ---
if player1_class == "warrior":
    player1 = create_warrior()
else:
    player1 = create_mage()
player1.name = player1_name
player1.x = WIDTH // 4 - CHAR_SIZE // 2
player1.y = HEIGHT // 2 - CHAR_SIZE // 2

if player2_class == "warrior":
    player2 = create_warrior()
else:
    player2 = create_mage()
player2.name = player2_name
player2.x = 3 * WIDTH // 4 - CHAR_SIZE // 2
player2.y = HEIGHT // 2 - CHAR_SIZE // 2

ability_message = ""
message_timer = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            
            # Only allow ability usage if game is not over
            if not game_over:
                # Player 1's turn
                if turn == 1:
                    if event.key == pygame.K_q:
                        result = player1.use_ability(0, player2)
                        ability_message = result
                        message_timer = 120
                        turn = 2  # Switch to Player 2's turn
                    if event.key == pygame.K_e:
                        result = player1.use_ability(1, player2)
                        ability_message = result
                        message_timer = 120
                        turn = 2  # Switch to Player 2's turn
                    if event.key == pygame.K_r:
                        print(f"R key pressed! Player 1 has {len(player1.abilities)} abilities")
                        print(f"Trying to use ability index 2...")
                        result = player1.use_ability(2, player1)
                        print(f"Result: {result}")
                        ability_message = result
                        message_timer = 120
                        turn = 2  # Switch to Player 2's turn
                    if event.key == pygame.K_f:
                        result = player1.use_ability(3, player1)
                        ability_message = result
                        message_timer = 120
                        turn = 2  # Switch to Player 2's turn

                # Player 2's turn
                if turn == 2:
                    if event.key == pygame.K_PERIOD:
                        result = player2.use_ability(0, player1)
                        ability_message = result
                        message_timer = 120
                        turn = 1  # Switch to Player 1's turn
                    if event.key == pygame.K_SLASH:
                        result = player2.use_ability(1, player1)
                        ability_message = result
                        message_timer = 120
                        turn = 1  # Switch to Player 1's turn
                    if event.key == pygame.K_QUOTE:
                        result = player2.use_ability(2, player2)
                        ability_message = result
                        message_timer = 120
                        turn = 1  # Switch to Player 1's turn
                    if event.key == pygame.K_HASH:
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

    # Draw background - ensure it completely fills the screen
    if background:
        # Clear screen first to prevent any bleed-through
        screen.fill((0, 0, 0))
        # Fill the entire screen with the background
        screen.blit(background, (0, 0))
    else:
        # Fallback: solid color background
        screen.fill((30, 30, 30))

    # Draw player 1
    if player1_class == "warrior" and warrior_img:
        screen.blit(warrior_img, (player1.x, player1.y))
    elif player1_class == "mage" and mage_img:
        screen.blit(mage_img, (player1.x, player1.y))
    else:
        pygame.draw.rect(screen, (255, 0, 0), (player1.x, player1.y, CHAR_SIZE, CHAR_SIZE))
    draw_health_bar(screen, player1.x, player1.y - 15, player1.health, player1.max_health)
    name1 = font.render(player1.name, True, (255, 255, 255))
    screen.blit(name1, (player1.x, player1.y - 35))

    # Draw player 2
    if player2_class == "warrior" and warrior_img:
        screen.blit(warrior_img, (player2.x, player2.y))
    elif player2_class == "mage" and mage_img:
        screen.blit(mage_img, (player2.x, player2.y))
    else:
        pygame.draw.rect(screen, (0, 0, 255), (player2.x, player2.y, CHAR_SIZE, CHAR_SIZE))
    draw_health_bar(screen, player2.x, player2.y - 15, player2.health, player2.max_health)
    name2 = font.render(player2.name, True, (255, 255, 255))
    screen.blit(name2, (player2.x, player2.y - 35))

    # --- Draw Abilities for Warrior (bottom left) and Mage (bottom right) ---
    ability_font = pygame.font.SysFont(None, 32)
    padding = 10
    ability_y = HEIGHT - 120  # Adjust as needed

    # Determine which player is the warrior and which is the mage
    if player1_class == "warrior":
        warrior = player1
        warrior_turn = (turn == 1)
        warrior_keys = ["Q", "E", "R", "F"]
        mage = player2
        mage_turn = (turn == 2)
        mage_keys = [".", "/", "'", "#"]
    else:
        warrior = player2
        warrior_turn = (turn == 2)
        warrior_keys = ["Q", "E", "R", "F"]
        mage = player1
        mage_turn = (turn == 1)
        mage_keys = [".", "/", "'", "#"]

    # Draw Warrior abilities (bottom left)
    for i, ability in enumerate(warrior.abilities):
        key = warrior_keys[i]
        text = f"{key}: {ability.name}"
        color = (255, 255, 0) if warrior_turn else (180, 180, 180)
        surf = ability_font.render(text, True, color)
        screen.blit(surf, (padding, ability_y + i * 32))

    # Draw Mage abilities (bottom right)
    for i, ability in enumerate(mage.abilities):
        key = mage_keys[i]
        text = f"{key}: {ability.name}"
        color = (0, 255, 255) if mage_turn else (180, 180, 180)
        surf = ability_font.render(text, True, color)
        screen.blit(surf, (WIDTH - surf.get_width() - padding, ability_y + i * 32))

    # Display game state
    if game_over and winner:
        # Victory screen
        victory_font = pygame.font.SysFont(None, 72)
        victory_msg = f"{winner.name} Wins!"
        victory_surface = victory_font.render(victory_msg, True, (255, 215, 0))  # Gold color
        screen.blit(victory_surface, (WIDTH // 2 - victory_surface.get_width() // 2, HEIGHT // 2 - 100))
        
        # Display winner's character image
        if winner == player1:
            if player1_class == "warrior" and warrior_img:
                winner_img = warrior_img
            elif player1_class == "mage" and mage_img:
                winner_img = mage_img
            else:
                winner_img = None
        else:  # winner == player2
            if player2_class == "warrior" and warrior_img:
                winner_img = warrior_img
            elif player2_class == "mage" and mage_img:
                winner_img = mage_img
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

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()