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
    background = pygame.image.load(r"C:\Users\brook\OneDrive\Desktop\code\Game\pygame_game\assets\background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except Exception as e:
    print("Failed to load background image:", e)
    background = None 
    
# Load and scale player images (optional) using absolute paths
CHAR_SIZE = 225  # Set this at the top
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

def character_selection(player_num):
    classes = ["Warrior", "Mage"]
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

        gap = WIDTH // 3
        for i, cls in enumerate(classes):
            x_pos = WIDTH // 2 - gap + i * (2 * gap)
            color = (255, 255, 0) if i == selected else (200, 200, 200)
            txt = font.render(cls, True, color)
            screen.blit(txt, (x_pos, 200))
            # Draw image preview
            if cls == "Warrior" and warrior_img:
                screen.blit(warrior_img, (x_pos, 260))
            elif cls == "Mage" and mage_img:
                screen.blit(mage_img, (x_pos, 260))

        if input_active:
            prompt = small_font.render("Enter your name (press Enter to confirm):", True, (255, 255, 255))
            screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 350))
            name_surface = font.render(name + "|", True, (0, 255, 0))
            screen.blit(name_surface, (WIDTH // 2 - name_surface.get_width() // 2, 400))

        pygame.display.flip()
        clock.tick(30)

    return classes[selected].lower(), name.strip() if name.strip() else classes[selected]

# --- Character selection for both players ---
player1_class, player1_name = character_selection(1)
player2_class, player2_name = character_selection(2)

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

player_speed = 5

# Optional: font for player names
font = pygame.font.SysFont(None, 24)

ability_message = ""
message_timer = 0  # To control how long the message is shown (in frames)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_q:
                result = player1.use_ability(0, player1)
                ability_message = result
                message_timer = 120  # Show for 2 seconds at 60 FPS
            if event.key == pygame.K_e:
                result = player1.use_ability(1, player1)
                ability_message = result
                message_timer = 120
            if event.key == pygame.K_r:
                result = player1.use_ability(2, player1)
                ability_message = result
                message_timer = 120
            if event.key == pygame.K_f:
                result = player1.use_ability(3, player1)

            if event.key == pygame.K_PERIOD:
                result = player2.use_ability(0, player2)
                ability_message = result
                message_timer = 120
            if event.key == pygame.K_SLASH:
                result = player2.use_ability(1, player2)
                ability_message = result
                message_timer = 120
            if event.key == pygame.K_QUOTE:
                result = player2.use_ability(2, player2)
                ability_message = result
                message_timer = 120
            if event.key == pygame.K_HASH:
                result = player2.use_ability(3, player2)
                ability_message = result
                message_timer = 120

    keys = pygame.key.get_pressed()
    # Player 1 (WASD)
    if keys[pygame.K_a]:
        player1.x -= player_speed
    if keys[pygame.K_d]:
        player1.x += player_speed
    if keys[pygame.K_w]:
        player1.y -= player_speed
    if keys[pygame.K_s]:
        player1.y += player_speed
    # Player 2 (Arrow keys)
    if keys[pygame.K_LEFT]:
        player2.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player2.x += player_speed
    if keys[pygame.K_UP]:
        player2.y -= player_speed
    if keys[pygame.K_DOWN]:
        player2.y += player_speed

    # Boundary checks
    player1.x = max(0, min(WIDTH - CHAR_SIZE, player1.x))
    player1.y = max(0, min(HEIGHT - CHAR_SIZE, player1.y))
    player2.x = max(0, min(WIDTH - CHAR_SIZE, player2.x))
    player2.y = max(0, min(HEIGHT - CHAR_SIZE, player2.y))

    # Draw background
    if background:
        screen.blit(background, (0, 0))
    else:
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