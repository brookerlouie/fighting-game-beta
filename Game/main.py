# main.py
# Entry point for your game

# Import your game modules here
# from game.engine import GameEngine

import pygame
import sys
from game.settings import WIDTH, HEIGHT
from game.entities import create_warrior, create_mage

pygame.init()
# Get the user's current screen size for fullscreen
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Fighting Game")
clock = pygame.time.Clock()

# Load and scale background image using absolute path
try:
    background = pygame.image.load(r"C:\Users\brook\OneDrive\Desktop\code\Game\game\assets\background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except Exception as e:
    print("Failed to load background image:", e)
    background = None  # If not found, fallback to fill color

# Load and scale player images (optional) using absolute paths
try:
    warrior_img = pygame.image.load(r"C:\Users\brook\OneDrive\Desktop\code\Game\game\assets\warrior.png")
    warrior_img = pygame.transform.scale(warrior_img, (50, 50))
except Exception as e:
    print("Failed to load warrior image:", e)
    warrior_img = None
try:
    mage_img = pygame.image.load(r"C:\Users\brook\OneDrive\Desktop\code\Game\game\assets\mage.png")
    mage_img = pygame.transform.scale(mage_img, (50, 50))
except Exception as e:
    print("Failed to load mage image:", e)
    mage_img = None

player1 = create_warrior()
player2 = create_mage()
player1.x, player1.y = 100, 100
player2.x, player2.y = 300, 100
player_speed = 5

def draw_health_bar(surface, x, y, current_health, max_health, width=50, height=8):
    pygame.draw.rect(surface, (60, 60, 60), (x, y, width, height))
    health_width = int(width * (current_health / max_health))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, health_width, height))
    pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 2)

# Optional: font for player names
font = pygame.font.SysFont(None, 24)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    keys = pygame.key.get_pressed()
    # Player 1 (arrows)
    if keys[pygame.K_LEFT]:
        player1.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player1.x += player_speed
    if keys[pygame.K_UP]:
        player1.y -= player_speed
    if keys[pygame.K_DOWN]:
        player1.y += player_speed
    # Player 2 (WASD)
    if keys[pygame.K_a]:
        player2.x -= player_speed
    if keys[pygame.K_d]:
        player2.x += player_speed
    if keys[pygame.K_w]:
        player2.y -= player_speed
    if keys[pygame.K_s]:
        player2.y += player_speed

    # Boundary checks
    player1.x = max(0, min(WIDTH - 50, player1.x))
    player1.y = max(0, min(HEIGHT - 50, player1.y))
    player2.x = max(0, min(WIDTH - 50, player2.x))
    player2.y = max(0, min(HEIGHT - 50, player2.y))

    # Draw background
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill((30, 30, 30))

    # Draw player 1
    if warrior_img:
        screen.blit(warrior_img, (player1.x, player1.y))
    else:
        pygame.draw.rect(screen, (255, 0, 0), (player1.x, player1.y, 50, 50))
    draw_health_bar(screen, player1.x, player1.y - 15, player1.health, player1.max_health)
    name1 = font.render(player1.name, True, (255, 255, 255))
    screen.blit(name1, (player1.x, player1.y - 35))

    # Draw player 2
    if mage_img:
        screen.blit(mage_img, (player2.x, player2.y))
    else:
        pygame.draw.rect(screen, (0, 0, 255), (player2.x, player2.y, 50, 50))
    draw_health_bar(screen, player2.x, player2.y - 15, player2.health, player2.max_health)
    name2 = font.render(player2.name, True, (255, 255, 255))
    screen.blit(name2, (player2.x, player2.y - 35))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
