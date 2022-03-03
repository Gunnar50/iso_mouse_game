from settings import *


def from_screen(screen_x, screen_y):
    ix = (screen_x - (ORIGIN_X * TILE_X)) / TILE_X
    iy = (screen_y - (ORIGIN_Y * TILE_Y)) / TILE_Y
    x = ix + iy
    y = iy - ix
    return x, y


def to_screen(x, y):
    screen_x = (ORIGIN_X * TILE_X) + (x - y) * (TILE_X / 2)
    screen_y = (ORIGIN_Y * TILE_Y) + (x + y) * (TILE_Y / 2)
    return screen_x, screen_y


print(to_screen(50, 20))
print(from_screen(1600, 1440))
