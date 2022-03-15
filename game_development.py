import time
import pygame
import sys
import math
from os import path
from settings import *
from sprites import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(400, 100)
        self.debug = {}
        self.mx, self.my = pygame.mouse.get_pos()
        self.sprite_sheet_image = pygame.image.load("isometric_whitebg - Copy.png").convert_alpha()
        self.index = 1
        self.mouse_held = False
        self.scroll_x, self.scroll_y = 0, 0
        self.start_pan_x, self.start_pan_y = 0, 0

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.sprite_sheet = SpriteSheet(self.sprite_sheet_image, self)
        self.tile_selected = self.sprite_sheet.get_image()[0]
        self.tiles = self.sprite_sheet.get_image()
        self.mouse_selection = MouseSelection(self, self.tile_selected)
        self.player = Player(self, (WIDTH/2)/TILE_X, (HEIGHT/2)/TILE_Y)
        self.trees = []

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
        if self.mouse_held:
            self.scroll_x -= self.mx - self.start_pan_x
            self.scroll_y -= self.my - self.start_pan_y
            self.start_pan_x = self.mx
            self.start_pan_y = self.my

        # -------------------------------------------------- CAMERA SCROLLING ----------------------------------------#
        if self.player.x - self.scroll_x != WIDTH/2:
            self.scroll_x += (self.player.x - (self.scroll_x + WIDTH/2))/10
            self.mx += self.scroll_x
        if self.player.y - self.scroll_y != HEIGHT/2:
            self.my += self.scroll_y
            self.scroll_y += (self.player.y - (self.scroll_y + HEIGHT/2))/10
        # -------------------------------------------------- CAMERA SCROLLING ----------------------------------------#

        self.debug_info()

    def to_screen(self, x, y):
        screen_x = (ORIGIN_X * TILE_X) + (x - y) * (TILE_X / 2)
        screen_y = (ORIGIN_Y * TILE_Y) + (x + y) * (TILE_Y / 2)
        return screen_x, screen_y

    def from_screen(self, screen_x, screen_y):
        ix = (screen_x - (ORIGIN_X * TILE_X)) / TILE_X
        iy = (screen_y - (ORIGIN_Y * TILE_Y)) / TILE_Y
        x = ix + iy
        y = iy - ix
        return x, y

    def draw_isogrid(self):
        for row in range(0, WIDTH, TILE_X):
            pygame.draw.line(self.screen, LIGHTGREY, (row-self.scroll_x, 0), (row-self.scroll_x, HEIGHT))
        for col in range(0, HEIGHT, TILE_Y):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col-self.scroll_y), (WIDTH, col-self.scroll_y))

        # start_x = 440
        # start_y = 40
        # for x, y in zip(range(start_x, WORLD_X * TILE_X, TILE_X // 2), range(start_y, WORLD_Y * TILE_Y, TILE_Y // 2)):
        #     pygame.draw.line(self.screen, RED, (x - self.scroll_x, y - self.scroll_y),
        #                      (x - WIDTH - self.scroll_x, y + WIDTH / 2 - self.scroll_y))
        #
        # for x, y in zip(range(start_x, -WIDTH, -TILE_X // 2), range(start_y, WIDTH, TILE_Y // 2)):
        #     pygame.draw.line(self.screen, RED, (x - self.scroll_x, y - self.scroll_y),
        #                      (x + WIDTH - self.scroll_x, y + WIDTH / 2 - self.scroll_y))

    def draw_world(self):
        for y in range(WORLD_Y):
            for x in range(WORLD_X):
                vWorld_x, vWorld_y = self.to_screen(x, y)
                # Invisible tile
                if self.index == 0:
                    self.screen.blit(self.tiles[1], (vWorld_x, vWorld_y))
                # Grass
                elif self.index == 1:
                    self.screen.blit(self.tiles[2], (vWorld_x-self.scroll_x, vWorld_y-self.scroll_y))

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.draw_world()
        #self.draw_isogrid()
        self.mouse_selection.draw()

        for tree in self.trees:
            self.screen.blit(self.tiles[4], (tree[0]-self.scroll_x, tree[1]-self.scroll_y))
        get_info(self.debug)
        pygame.display.flip()

    def debug_info(self):
        mx, my = self.from_screen(self.mx, self.my)
        self.debug["FPS"] = int(self.clock.get_fps())
        self.debug["Cell"] = self.mouse_selection.cell_x, self.mouse_selection.cell_y
        self.debug["Selected"] = int(self.mouse_selection.selected_x), int(self.mouse_selection.selected_y)
        self.debug["Scroll"] = int(self.scroll_x), int(self.scroll_y)
        self.debug["Mouse"] = int(self.mx), int(self.my)
        self.debug["Mouse_offset"] = int(self.mouse_selection.offset_x), int(self.mouse_selection.offset_y)
        self.debug["MouseIso"] = int(mx), int(my)

        # self.debug["Color"] = self.screen.get_at((self.mx, self.my))


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
                    self.clicked_x, self.clicked_y = self.to_screen(self.mouse_selection.selected_x,
                                                                    self.mouse_selection.selected_y)
                    self.trees.append((self.clicked_x, self.clicked_y))

                if event.button == 3:
                    self.start_pan_x = self.mx
                    self.start_pan_y = self.my
                    self.mouse_held = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.mouse_held = False


game = Game()
while True:
    game.new()
    game.run()
