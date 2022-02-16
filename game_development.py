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
        self.camera = Camera()

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
        # -------------------------------------------------- CAMERA SCROLLING ----------------------------------------#
        if self.player.x - self.scroll_x != WIDTH/2:
            self.scroll_x += (self.player.x - (self.scroll_x + WIDTH/2))/10
        if self.player.y - self.scroll_y != HEIGHT/2:
            self.scroll_y += (self.player.y - (self.scroll_y + HEIGHT/2))/10
        # -------------------------------------------------- CAMERA SCROLLING ----------------------------------------#
        self.camera.update()
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
                    self.screen.blit(self.tiles[2], (vWorld_x-self.scroll_x, vWorld_y-self.scroll_y))
                    #self.screen.blit(self.tiles[2], (vWorld_x + self.camera.scroll.x, vWorld_y + self.camera.scroll.y))

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


# create the game object
game = Game()
while True:
    game.new()
    game.run()
