import pygame

pygame.init()
WIDTH = 800
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
scroll_x, scroll_y = 0, 0
global game_map


colors = {'g': (40, 128, 40), 'd': (90, 60, 40)}
tilemap = [
    'gdddg',
    'dgddd',
    'ggddg',
    'ggddg',
    'ddddg',
    'dgggd'
]
columns, rows = len(tilemap[0]), len(tilemap)

isometric_tiles = {}
for key, color in colors.items():
    tile_surf = pygame.Surface((50, 50), pygame.SRCALPHA)
    tile_surf.fill(color)
    tile_surf = pygame.transform.rotate(tile_surf, 45)
    isometric_size = tile_surf.get_width()
    tile_surf = pygame.transform.scale(tile_surf, (isometric_size, isometric_size // 2))
    isometric_tiles[key] = tile_surf
tile_size = (isometric_size, isometric_size // 2)


def to_screen(x, y):
    ORIGIN_X = 5
    ORIGIN_Y = 1
    screen_x = (ORIGIN_X * isometric_size) + (x - y) * (isometric_size / 2)
    screen_y = (ORIGIN_Y * (isometric_size // 2)) + (x + y) * ((isometric_size // 2) / 2)
    return screen_x, screen_y

def tileRect(column, row, tile_size):
    x = (column + row) * tile_size[0] // 2
    y = ((columns - column - 1) + row) * tile_size[1] // 2
    return pygame.Rect(x, y, *tile_size)


def draw_tiles():
    global game_map
    game_map = pygame.Surface(((columns + rows) * isometric_size // 2, (columns + rows) * isometric_size // 4),
                              pygame.SRCALPHA)
    for column in range(columns):
        for row in range(rows):
            tile_surf = isometric_tiles[tilemap[row][column]]
            column_1, row_1 = to_screen(column, row)
            tile_rect = tileRect(column_1-scroll_x, row_1-scroll_y, tile_size)
            game_map.blit(tile_surf, tile_rect)

draw_tiles()
map_rect = game_map.get_rect(center=window.get_rect().center)
map_outline = [
    pygame.math.Vector2(0, columns * isometric_size / 4),
    pygame.math.Vector2(columns * isometric_size / 2, 0),
    pygame.math.Vector2((columns + rows) * isometric_size // 2, rows * isometric_size / 4),
    pygame.math.Vector2(rows * isometric_size / 2, (columns + rows) * isometric_size // 4)
]
for pt in map_outline:
    pt += map_rect.topleft

origin = map_outline[0]
x_axis = (map_outline[1] - map_outline[0]) / columns
y_axis = (map_outline[3] - map_outline[0]) / rows


def inverseMat2x2(m):
    a, b, c, d = m[0].x, m[0].y, m[1].x, m[1].y
    det = 1 / (a * d - b * c)
    return [(d * det, -b * det), (-c * det, a * det)]


point_to_grid = inverseMat2x2((x_axis, y_axis))


def transform(p, mat2x2):
    x = p[0] * mat2x2[0][0] + p[1] * mat2x2[1][0]
    y = p[0] * mat2x2[0][1] + p[1] * mat2x2[1][1]
    return pygame.math.Vector2(x, y)


font = pygame.font.SysFont(None, 30)
textO = font.render("O", True, (255, 255, 255))
textX = font.render("X", True, (255, 0, 0))
textY = font.render("Y", True, (0, 255, 0))

p_col, p_row = 2, 2




class Player:
    def __init__(self, x, y):
        self.x, self.y = to_screen(x, y)
        print(x, y)
        self.vx, self.vy = 0, 0

    def update(self, dt):
        self.get_keys()
        self.x += self.vx * dt
        self.y += self.vy * dt

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


pygame.key.set_repeat(400, 100)
PLAYER_SPEED = 300

player = Player((WIDTH / 2) / isometric_size, (HEIGHT / 2) / isometric_size//2)
run = True
while run:
    dt = clock.tick(100)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and p_col > 0:
                p_col -= 1
            if event.key == pygame.K_d and p_col < columns - 1:
                p_col += 1
            if event.key == pygame.K_w and p_row > 0:
                p_row -= 1
            if event.key == pygame.K_s and p_row < rows - 1:
                p_row += 1

    p_position = transform((p_col + 0.5, p_row + 0.5), (x_axis, y_axis)) + origin
    m_pos = pygame.mouse.get_pos()
    m_grid_pos = transform(pygame.math.Vector2(m_pos) - origin, point_to_grid)
    m_col, m_row = int(m_grid_pos[0]), int(m_grid_pos[1])

    player.update(dt)
    # -------------------------------------------------- CAMERA SCROLLING ----------------------------------------#
    if player.x - scroll_x != WIDTH / 2:
        scroll_x += (player.x - (scroll_x + WIDTH / 2)) / 10
    if player.y - scroll_y != HEIGHT / 2:
        scroll_y += (player.y - (scroll_y + HEIGHT / 2)) / 10
    # -------------------------------------------------- CAMERA SCROLLING ----------------------------------------#

    draw_tiles()

    window.fill((0, 0, 0))
    window.blit(game_map, map_rect)
    pygame.draw.lines(window, (164, 164, 164), True, map_outline, 3)
    pygame.draw.line(window, (255, 0, 0), origin, origin + x_axis, 3)
    pygame.draw.line(window, (0, 255, 0), origin, origin + y_axis, 3)
    pygame.draw.circle(window, (255, 255, 255), origin, 5)
    pygame.draw.circle(window, (255, 0, 0), origin + x_axis, 5)
    pygame.draw.circle(window, (0, 255, 0), origin + y_axis, 5)
    window.blit(textO, textO.get_rect(topright=origin + (-5, 5)))
    window.blit(textX, textX.get_rect(bottomright=origin + x_axis + (-5, -5)))
    window.blit(textY, textX.get_rect(topright=origin + y_axis + (-5, 5)))
    # pygame.draw.ellipse(window, (255, 255, 0), (p_position[0] - 16, p_position[1] - 8, 32, 16))
    if 0 <= m_grid_pos[0] < columns and 0 <= m_grid_pos[1] < rows:
        tile_rect = tileRect(m_col, m_row, tile_size).move(map_rect.topleft)
        pts = [tile_rect.midleft, tile_rect.midtop, tile_rect.midright, tile_rect.midbottom]
        pygame.draw.lines(window, (255, 255, 255), True, pts, 4)
    pygame.display.update()

pygame.quit()
exit()
