import pygame
from settings import *
from pygame.math import Vector2


class Player:
    def __init__(self, game, x, y):
        self.game = game
        self.x, self.y = self.game.to_screen(x, y)
        self.vx, self.vy = 0, 0

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pygame.K_s]:
            self.vy = PLAYER_SPEED
        if keys[pygame.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pygame.K_d]:
            self.vx = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 1.0
            self.vy *= 0.50


class MouseSelection:
    def __init__(self, game, image):
        self.game = game
        self.image = image

    def update(self):
        # get mouse x and y
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        # get the mouse offset position inside the tile
        self.offset_x, self.offset_y = self.mouse_x % TILE_X, self.mouse_y % TILE_Y
        self.offset_x += self.game.scroll_x % TILE_X
        self.offset_y += self.game.scroll_y % TILE_Y

        # get the cell number
        self.cell_x, self.cell_y = (self.mouse_x // TILE_X), (self.mouse_y // TILE_Y)
        self.cell_x += int((self.game.scroll_x//TILE_X))
        self.cell_y += int((self.game.scroll_y//TILE_Y))



        # get the selected cell in iso grid
        self.selected_x = (self.cell_y - ORIGIN_Y) + (self.cell_x - ORIGIN_X)
        self.selected_y = (self.cell_y - ORIGIN_Y) - (self.cell_x - ORIGIN_X)


        # height and width of a quarter of a tile, select the corner of the tile to nodge to a direction
        h, w = TILE_Y/2, TILE_X/2
        if self.offset_y < (h / w) * (w - self.offset_x):
            self.selected_x -= 1
        if self.offset_y > (h / w) * self.offset_x + h:
            self.selected_y += 1
        if self.offset_y < (h / w) * self.offset_x - h:
            self.selected_y -= 1
        if self.offset_y > (h / w) * (2 * w - self.offset_x) + h:
            self.selected_x += 1

        # colour = self.game.screen.get_at((self.mouse_x, self.mouse_y))
        # if colour == RED:
        #     self.selected_x -= 1
        # if colour == BLUE:
        #     self.selected_y -= 1
        # if colour == GREEN:
        #     self.selected_y += 1
        # if colour == YELLOW:
        #     self.selected_x += 1

        # translate the selected cell to world coordinate
        self.selectedWorld_x, self.selectedWorld_y = self.game.to_screen(self.selected_x,
                                                                         self.selected_y)

    def draw(self):
        self.game.screen.blit(self.image, (self.selectedWorld_x-self.game.scroll_x,
                                           self.selectedWorld_y-self.game.scroll_y))


class SpriteSheet:
    def __init__(self, image, game):
        self.image = image
        self.frames = []
        self.game = game

    def get_image(self):
        for row in range(2):
            for col in range(4):
                if row == 0:
                    image = pygame.Surface((TILE_Y, TILE_Y / 2)).convert_alpha()
                    image.blit(self.image, (0, 0), (col * TILE_X / 2, row * TILE_Y / 2, TILE_X, TILE_Y))
                    image = pygame.transform.scale(image, (TILE_X, TILE_Y))
                else:
                    image = pygame.Surface((TILE_Y, TILE_Y)).convert_alpha()
                    image.blit(self.image, (0, 0), (col * TILE_X/2, row * TILE_Y/2, TILE_X, TILE_Y*2))
                    image = pygame.transform.scale(image, (TILE_X, TILE_Y*2))
                image.set_colorkey(WHITE)
                self.frames.append(image)
        return self.frames


