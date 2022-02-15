import pygame
from settings import *

pygame.init()
font = pygame.font.Font(None, 25)


def debug(info, y, x=10):
    display_surface = pygame.display.get_surface()
    debug_surface = font.render(str(info), True, WHITE)
    debug_rect = debug_surface.get_rect(topleft=(x, y))
    display_surface.blit(debug_surface, debug_rect)
