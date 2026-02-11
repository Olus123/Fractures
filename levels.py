import pygame
import csv

TILE_SIZE = 32  # Match your Tiled tileset size

def load_csv(filename):
    """Load CSV and return a 2D list of ints."""
    grid = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            grid.append([int(cell) for cell in row])
    return grid

def load_tileset_image(image_file):
    """Load tileset image and slice into individual tiles."""
    tileset = pygame.image.load(image_file).convert_alpha()
    tiles = []
    tileset_width, tileset_height = tileset.get_size()
    for y in range(0, tileset_height, TILE_SIZE):
        for x in range(0, tileset_width, TILE_SIZE):
            tile = tileset.subsurface(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            tiles.append(tile)
    return tiles

class Level:
    def __init__(self, background_csv, platforms_csv, collectibles_csv,
                 background_image, platforms_image, collectibles_image):

        # Load CSVs
        self.background_grid = load_csv(background_csv)
        self.platforms_grid = load_csv(platforms_csv)
        self.collectibles_grid = load_csv(collectibles_csv)

        # Load tileset images
        self.background_tiles = load_tileset_image(background_image)
        self.platform_tiles = load_tileset_image(platforms_image)
        self.collectible_tiles = load_tileset_image(collectibles_image)

        # List to track collectible rects
        self.collectible_rects = []
        self.populate_collectibles()

    def populate_collectibles(self):
        """Create rects for each collectible on the map."""
        self.collectible_rects = []
        for row_index, row in enumerate(self.collectibles_grid):
            for col_index, tile_id in enumerate(row):
                if tile_id >= 0:
                    rect = pygame.Rect(col_index * TILE_SIZE,
                                       row_index * TILE_SIZE,
                                       TILE_SIZE, TILE_SIZE)
                    self.collectible_rects.append((rect, tile_id))

    def draw(self, screen):
        # Draw background
        for row_index, row in enumerate(self.background_grid):
            for col_index, tile_id in enumerate(row):
                if tile_id >= 0:
                    tile = self.background_tiles[tile_id]
                    screen.blit(tile, (col_index * TILE_SIZE, row_index * TILE_SIZE))

        # Draw platforms
        for row_index, row in enumerate(self.platforms_grid):
            for col_index, tile_id in enumerate(row):
                if tile_id >= 0:
                    tile = self.platform_tiles[tile_id]
                    screen.blit(tile, (col_index * TILE_SIZE, row_index * TILE_SIZE))

        # Draw collectibles
        for rect, tile_id in self.collectible_rects:
            tile = self.collectible_tiles[tile_id]
            screen.blit(tile, rect.topleft)