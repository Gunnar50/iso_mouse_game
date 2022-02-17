import time
import pygame
import sys
import math
from os import path
from settings import *
from sprites import *

# ------------------------- SETTINGS ---------------------------- #
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


# ------------------------- SPRITES ---------------------------- #

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

        # get the cell number
        self.cell_x, self.cell_y = (self.mouse_x // TILE_X), (self.mouse_y // TILE_Y)
        self.cell_x += (self.game.scroll_x//TILE_X)+0.5
        self.cell_y += (self.game.scroll_y//TILE_Y)+0.5


        # get the selected cell in iso grid
        self.selected_x = (self.cell_y - ORIGIN_Y) + (self.cell_x - ORIGIN_X)
        self.selected_y = (self.cell_y - ORIGIN_Y) - (self.cell_x - ORIGIN_X)

        # height and width of a quarter of a tile, select the corner of the tile to nodge to a direction
        h, w = TILE_Y / 2, TILE_X / 2
        if self.offset_y < (h / w) * (w - self.offset_x):
            self.selected_x -= 1
        if self.offset_y > (h / w) * self.offset_x + h:
            self.selected_y += 1
        if self.offset_y < (h / w) * self.offset_x - h:
            self.selected_y -= 1
        if self.offset_y > (h / w) * (2 * w - self.offset_x) + h:
            self.selected_x += 1

        # translate the selected cell to world coordinate
        self.selectedWorld_x, self.selectedWorld_y = self.game.to_screen(self.selected_x, self.selected_y)

    def draw(self):
        self.game.screen.blit(self.image, (self.selectedWorld_x-self.game.scroll_x, self.selectedWorld_y-self.game.scroll_y))
#testcomment#

class SpriteSheet:
    def __init__(self, image):
        self.image = image
        self.frames = []

    def get_image(self):
        for row in range(2):
            for col in range(4):
                if row == 0:
                    image = pygame.Surface((TILE_Y, TILE_Y / 2)).convert_alpha()
                    image.blit(self.image, (0, 0), (col * TILE_X / 2, row * TILE_Y / 2, TILE_X, TILE_Y))
                    image = pygame.transform.scale(image, (TILE_X, TILE_Y))
                else:
                    image = pygame.Surface((TILE_Y, TILE_Y)).convert_alpha()
                    image.blit(self.image, (0, 0), (col * TILE_X / 2, row * TILE_Y / 2, TILE_X, TILE_Y * 2))
                    image = pygame.transform.scale(image, (TILE_X, TILE_Y * 2))
                image.set_colorkey(WHITE)
                self.frames.append(image)
        return self.frames


# ------------------------- GAME LOOP ---------------------------- #
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(400, 100)
        self.debug = {}
        self.sprite_sheet_image = pygame.image.load("isometric_whitebg.png")
        self.index = 1
        self.scroll_x, self.scroll_y = 0, 0

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.sprite_sheet = SpriteSheet(self.sprite_sheet_image)
        self.tile_selected = self.sprite_sheet.get_image()[0]
        self.tiles = self.sprite_sheet.get_image()
        self.mouse_selection = MouseSelection(self, self.tile_selected)
        self.player = Player(self, 1, 1)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.player.update()
        self.mouse_selection.update()
        self.mx, self.my = pygame.mouse.get_pos()

        # -------------------------------------------------- KEYBOARD SCROLLING ----------------------------------------#
        if self.player.x - self.scroll_x != WIDTH / 2:
            self.scroll_x += (self.player.x - (self.scroll_x + WIDTH / 2)) / 10
        if self.player.y - self.scroll_y != HEIGHT / 2:
            self.scroll_y += (self.player.y - (self.scroll_y + HEIGHT / 2)) / 10
        # --------------------------------------------------------------------------------------------------------------#

        #----------------------------------------------------MOUSE SCROLLING--------------------------------------------#
        #if the mouse is close to the edge of the resolution, add/decrease scroll#
        if self.mx > 880:
            scroll_amountX = 5
        elif self.mx < 150:
            scroll_amountX = -5
        else:
            scroll_amountX = 0

        if self.my < 125:
            scroll_amountY = -4
        elif self.my > 620:
            scroll_amountY = 4
        else:
            scroll_amountY = 0

        self.scroll_x += scroll_amountX
        self.player.x += scroll_amountX
        self.scroll_y += scroll_amountY
        self.player.y += scroll_amountY
        #---------------------------------------------------------------------------------------------------------------#

        self.debug_info()

    def to_screen(self, x, y):
        screen_x = (ORIGIN_X * TILE_X) + (x - y) * (TILE_X / 2)
        screen_y = (ORIGIN_Y * TILE_Y) + (x + y) * (TILE_Y / 2)
        return screen_x, screen_y

    def draw_world(self):
        for y in range(WORLD_Y):
            for x in range(WORLD_X):
                vWorld_x, vWorld_y = self.to_screen(x, y)
                # Invisible tile
                if self.index == 0:
                    self.screen.blit(self.tiles[1], (vWorld_x, vWorld_y))
                # Grass
                elif self.index == 1:
                    self.screen.blit(self.tiles[2], (vWorld_x - self.scroll_x, vWorld_y - self.scroll_y))

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.draw_world()
        self.mouse_selection.draw()

        get_info(self.debug)
        pygame.display.flip()

    def debug_info(self):
        self.debug["FPS"] = int(self.clock.get_fps())
        self.debug["Cell"] = self.mouse_selection.cell_x, self.mouse_selection.cell_y
        self.debug["Selected"] = int(self.mouse_selection.selected_x), int(self.mouse_selection.selected_y)
        self.debug["Scroll"] = int(self.scroll_x), int(self.scroll_y)
        self.debug["Mouse"] = int(self.mx), int(self.my)
        self.debug["Mouse_offset"] = int(self.mouse_selection.offset_x), int(self.mouse_selection.offset_y)

    def events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pass


game = Game()
while True:
    game.new()
    game.run()
