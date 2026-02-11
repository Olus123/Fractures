import pygame
from menu import Menu
from player import Player
from levels import Level

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fractures - Prototype 3")

# Clock for controlling FPS
clock = pygame.time.Clock()
FPS = 60

# Initialize game components
menu = Menu(screen)
player = Player(100, 500)  # Starting position

# Load first level
level1 = Level(
    "levels/level1_background.csv",
    "levels/level1_platforms.csv",
    "levels/level1_collectibles.csv",
    "tilesets/background.png",
    "tilesets/platforms.png",
    "tilesets/collectible.png"
)

# Game states
STATE_MENU = "menu"
STATE_PLAYING = "playing"
game_state = STATE_MENU

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == STATE_MENU:
            menu.handle_event(event)

        elif game_state == STATE_PLAYING:
            player.handle_event(event)

    # Update game logic
    if game_state == STATE_PLAYING:
        player.update()

        # Check collectible collisions
        new_collectibles = []
        for rect, tile_id in level1.collectible_rects:
            if player.rect.colliderect(rect):
                # collected, skip adding back
                continue
            new_collectibles.append((rect, tile_id))
        level1.collectible_rects = new_collectibles

    # Draw everything
    screen.fill((135, 206, 250))  # Sky-blue background

    if game_state == STATE_MENU:
        menu.draw()
        if menu.start_game_selected:
            game_state = STATE_PLAYING

    elif game_state == STATE_PLAYING:
        level1.draw(screen)
        player.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()