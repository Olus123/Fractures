# menu.py
import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 50)
        self.start_game_selected = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.start_game_selected = True

    def draw(self):
        self.screen.fill((50, 50, 50))
        text = self.font.render("Press ENTER to Start Game", True, (255, 255, 255))
        self.screen.blit(text, (100, 250))