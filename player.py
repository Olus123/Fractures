import pygame

GRAVITY = 0.5

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

    def handle_event(self, event):
        pass

    def update(self, level):
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

        # Update rect
        self.rect.topleft = (self.x, self.y)
        self.on_ground = False

        # Collision with platforms
        for tile in level.platforms:
            if self.rect.colliderect(tile):
                # Falling
                if self.vel_y > 0 and self.rect.bottom - self.vel_y <= tile.top:
                    self.y = tile.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                # Jumping up
                elif self.vel_y < 0 and self.rect.top - self.vel_y >= tile.bottom:
                    self.y = tile.bottom
                    self.vel_y = 0
                # Left
                elif self.x + self.width > tile.left and self.x < tile.left:
                    self.x = tile.left - self.width
                # Right
                elif self.x < tile.right and self.x + self.width > tile.right:
                    self.x = tile.right

        # Clamp to screen
        if self.x < 0: self.x = 0
        if self.x + self.width > 800: self.x = 800 - self.width
        if self.y + self.height > 600:
            self.y = 600 - self.height
            self.vel_y = 0
            self.on_ground = True

        self.rect.topleft = (self.x, self.y)

        # Check collectibles
        for c in level.collectibles:
            if not c['collected'] and self.rect.colliderect(c['rect']):
                c['collected'] = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
