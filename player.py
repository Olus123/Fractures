# player.py
import pygame

GRAVITY = 0.5  # Gravity applied to player

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.color = (255, 0, 0)
        self.speed = 5
        self.vel_y = 0
        self.jump_strength = 10
        self.on_ground = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

         # Simple tile platforms (x, y, width, height)
        self.tiles = [
            pygame.Rect(100, 500, 600, 20),  # Ground
            pygame.Rect(300, 400, 150, 20),  # Platform 1
            pygame.Rect(150, 300, 150, 20)   # Platform 2
        ]

    def handle_event(self, event):
        pass  # No event-specific logic for now

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -self.jump_strength
            self.on_ground = False

        # Apply gravity
        self.vel_y += GRAVITY
        self.y += self.vel_y

        # Update player rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.on_ground = False

        # Check collisions with tiles
        for tile in self.tiles:
            if self.rect.colliderect(tile):
                # Player falling onto tile
                if self.vel_y > 0 and self.rect.bottom - self.vel_y <= tile.top:
                    self.y = tile.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                # Player hitting tile from below
                elif self.vel_y < 0 and self.rect.top - self.vel_y >= tile.bottom:
                    self.y = tile.bottom
                    self.vel_y = 0
                # Player colliding from left
                elif self.x + self.width > tile.left and self.x < tile.left and \
                    self.y + self.height > tile.top and self.y < tile.bottom:
                    self.x = tile.left - self.width
                # Player colliding from right
                elif self.x < tile.right and self.x + self.width > tile.right and \
                    self.y + self.height > tile.top and self.y < tile.bottom:
                    self.x = tile.right

        # Prevent moving out of screen bounds
        if self.x < 0:
            self.x = 0
        if self.x + self.width > 800:
            self.x = 800 - self.width
        if self.y + self.height > 600:
            self.y = 600 - self.height
            self.vel_y = 0
            self.on_ground = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Draw tiles
        for tile in self.tiles:
            pygame.draw.rect(screen, (0, 255, 0), tile)