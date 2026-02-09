import pygame
from menu import Menu
from player import Player
from levels import Level

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fractures - Prototype 3")

clock = pygame.time.Clock()
FPS = 60

menu = Menu(screen)
player = Player(100, 500)  # Starting position

# Load level 1
level1 = Level(
    "level1_background.csv",
    "level1_platforms.csv",
    "level1_collectibles.csv",
    "tilesets/level1_tiles.png",
    32
)

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

    if game_state == STATE_PLAYING:
        player.update(level1)

    screen.fill((135, 206, 250))  # Sky-blue

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