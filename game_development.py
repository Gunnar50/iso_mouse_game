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
        self.sprite_sheet_image = pygame.image.load("isometric_whitebg.png")
        self.index = 1
        self.scroll_x, self.scroll_y = 0, 0

    def load_map(self):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, "map_test.txt"))
        self.trees = []
        self.floors = []
        for row in range(len(self.map.data)):
            for col in range(len(self.map.data[row])):
                self.floors.append(Floor(self, col, row))
                if self.map.data[row][col] == "1":
                    self.trees.append(Tree(self, col, row))
                if self.map.data[row][col] == "P":
                    self.player = Player(self, col, row, self.tile_selected)

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
        # -------------------------------------------------- CAMERA SCROLLING ----------------------------------------#
        if self.player.x - self.scroll_x != WIDTH/2:
            self.scroll_x += (self.player.x - (self.scroll_x + WIDTH/2))/10
        if self.player.y - self.scroll_y != HEIGHT/2:
            self.scroll_y += (self.player.y - (self.scroll_y + HEIGHT/2))/10
        # -------------------------------------------------- CAMERA SCROLLING ----------------------------------------#

    def to_screen(self, x, y):
        screen_x = (ORIGIN_X * TILE_X) + (x - y) * (TILE_X / 2)
        screen_y = (ORIGIN_Y * TILE_Y) + (x + y) * (TILE_Y / 2)
        return screen_x, screen_y

    def draw_grid(self):
        # for row in range(0, WIDTH, TILE_X):
        #     pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, HEIGHT))
        # for col in range(0, HEIGHT, TILE_Y):
        #     pygame.draw.line(self.screen, LIGHTGREY, (0, col), (WIDTH, col))

        # -------------------------------------------------- ISOMETRIC GRID ------------------------------------------#
        start_x = 440
        start_y = 40
        for x, y in zip(range(start_x, WORLD_X * TILE_X, TILE_X // 2), range(start_y, WORLD_Y * TILE_Y, TILE_Y // 2)):
            pygame.draw.line(self.screen, RED, (x - self.scroll_x, y - self.scroll_y),
                             (x - WIDTH - self.scroll_x, y + WIDTH / 2 - self.scroll_y))

        for x, y in zip(range(start_x, -WIDTH, -TILE_X // 2), range(start_y, WIDTH, TILE_Y // 2)):
            pygame.draw.line(self.screen, RED, (x - self.scroll_x, y - self.scroll_y),
                             (x + WIDTH - self.scroll_x, y + WIDTH / 2 - self.scroll_y))
        # -------------------------------------------------- ISOMETRIC GRID ------------------------------------------#

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

    def draw_floor_tiles(self):
        # -------------------------------------------------- FLOOR TILES ------------------------------------------#
        top_x = 5 * TILE_X + TILE_X / 2
        top_y = TILE_Y
        bottom_x = 5 * TILE_X + TILE_X / 2
        bottom_y = 2 * TILE_Y
        left_x = 5 * TILE_X
        left_y = TILE_Y + TILE_Y / 2
        right_x = 6 * TILE_X
        right_y = TILE_Y + TILE_Y / 2
        overflow = 200  # overflow value in pixel to overflow the screen

        for j in range(200):
            for i in range(200):
                # if statement to only render the tiles that are visible to the player
                if self.player.x + WIDTH/2 + overflow > (top_x + i * (TILE_X / 2)) > self.player.x - WIDTH/2 - overflow and \
                        self.player.y + HEIGHT/2 + overflow > (top_y + i * (TILE_Y / 2)) > self.player.y - HEIGHT/2 - overflow:
                    pygame.draw.polygon(self.screen, LIGHTGREY,
                                        ((top_x + i * (TILE_X / 2) - self.scroll_x,
                                          top_y + i * (TILE_Y / 2) - self.scroll_y),
                                         (right_x + i * (TILE_X / 2) - self.scroll_x,
                                          right_y + i * (TILE_Y / 2) - self.scroll_y),
                                         (bottom_x + i * (TILE_X / 2) - self.scroll_x,
                                          bottom_y + i * (TILE_Y / 2) - self.scroll_y),
                                         (left_x + i * (TILE_X / 2) - self.scroll_x,
                                          left_y + i * (TILE_Y / 2) - self.scroll_y)))

            top_x -= TILE_X / 2
            top_y += TILE_Y / 2
            bottom_x -= TILE_X / 2  # FLOOR TILES
            bottom_y += TILE_Y / 2
            left_x -= TILE_X / 2
            left_y += TILE_Y / 2
            right_x -= TILE_X / 2
            right_y += TILE_Y / 2
        # -------------------------------------------------- FLOOR TILES ------------------------------------------#

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.draw_world()
        self.mouse_selection.draw()
        # self.player.draw()

        # pygame.draw.rect(self.screen, RED, (self.cell_x * TILE_X, self.cell_y * TILE_Y, TILE_X, TILE_Y), 2)

        # debug
        debug(f"FPS     {round(self.clock.get_fps())}", 10)
        debug(f"Cell         {self.mouse_selection.cell_x, self.mouse_selection.cell_y}", 40)
        debug(f"Selected {self.mouse_selection.selected_x, self.mouse_selection.selected_y}", 70)
        debug(f"Scroll      {round(self.scroll_x), round(self.scroll_y)}", 100)
        # debug(f"Player      {int(self.player.x), int(self.player.y)}", 100)
        # debug(f"Player Speed  {PLAYER_SPEED}", 400)

        pygame.display.flip()

    def events(self):
        global PLAYER_SPEED
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("a")

    def show_start_screen(self):
        pass


# create the game object
game = Game()
game.show_start_screen()
while True:
    game.new()
    game.run()
