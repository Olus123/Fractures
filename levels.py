# levels.py
import pygame
import csv

TILE_SIZE = 32  # Adjust based on your tileset tiles

def load_csv(filename):
    """Load a CSV file and return a 2D list of integers"""
    grid = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            grid.append([int(cell) for cell in row])
    return grid

def load_tileset(filename):
    """Load a tileset image and slice it into individual tile surfaces"""
    image = pygame.image.load(filename).convert_alpha()
    tiles = []
    image_width, image_height = image.get_size()
    for y in range(0, image_height, TILE_SIZE):
        for x in range(0, image_width, TILE_SIZE):
            tile = image.subsurface(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            tiles.append(tile)
    return tiles

class Level:
    def __init__(self, background_file, Platforms_file, collectibles_file,
                 background_image, Platforms_image, collectibles_image):
        # Load CSVs
        self.background_grid = load_csv(background_file)
        self.Platforms_grid = load_csv(Platforms_file)
        self.collectibles_grid = load_csv(collectibles_file)

        # Load tilesets
        self.background_tiles = load_tileset(background_image)
        self.platform_tiles = load_tileset(Platforms_image)
        self.collectible_tiles = load_tileset(collectibles_image)

        # List of active collectibles for collision detection
        self.active_collectibles = []

        # Convert CSV data into rects with positions
        self.platform_rects = []
        for row_index, row in enumerate(self.Platforms_grid):
            for col_index, tile_id in enumerate(row):
                if tile_id >= 0:
                    rect = pygame.Rect(col_index * TILE_SIZE,
                                       row_index * TILE_SIZE,
                                       TILE_SIZE, TILE_SIZE)
                    self.platform_rects.append((rect, tile_id))

        for row_index, row in enumerate(self.collectibles_grid):
            for col_index, tile_id in enumerate(row):
                if tile_id >= 0:
                    rect = pygame.Rect(col_index * TILE_SIZE,
                                       row_index * TILE_SIZE,
                                       TILE_SIZE, TILE_SIZE)
                    self.active_collectibles.append((rect, tile_id))

    def draw(self, screen):
        # Draw background
        for row_index, row in enumerate(self.background_grid):
            for col_index, tile_id in enumerate(row):
                if tile_id >= 0:
                    tile_image = self.background_tiles[tile_id]
                    screen.blit(tile_image, (col_index * TILE_SIZE,
                                             row_index * TILE_SIZE))
        # Draw Platforms
        for rect, tile_id in self.platform_rects:
            screen.blit(self.platform_tiles[tile_id], rect.topleft)

        # Draw collectibles
        for rect, tile_id in self.active_collectibles:
            screen.blit(self.collectible_tiles[tile_id], rect.topleft)
