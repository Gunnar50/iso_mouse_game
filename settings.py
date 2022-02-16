import pygame
# COLORS (r, g, b)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
title = "Tile-Based game"
BGCOLOUR = DARKGREY

TILE_X = 80
TILE_Y = 40

WORLD_X, WORLD_Y = 14, 10
ORIGIN_X, ORIGIN_Y = 5, 1

# Debug
pygame.init()
font = pygame.font.Font(None, 25)

PLAYER_SPEED = 300


def get_info(info_list):
    display_surface = pygame.display.get_surface()
    for i, key in enumerate(info_list):
        text = font.render(str(key) + " : " + str(info_list[key]), True, (255, 255, 255), (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.y = 20 * i
        display_surface.blit(text, text_rect)
