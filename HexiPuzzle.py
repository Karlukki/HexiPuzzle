import pygame as pg
from grids.src.updown_tri import *

tri_grid_coords = [
    {(0, 2, 0), (0, 1, 0), (0, 1, 1), (1, 1, 0), (0, 0, 1), (1, 0, 0)}, #A
    {(-1, 2, 1), (-1, 1, 1), (0, 1, 1), (0, 1, 0), (0, 0, 1), (1, 0, 1)},#E
    {(0, 1, 1), (0, 1, 0), (1, 1, 0), (0, 0, 2), (0, 0, 1), (1, 0, 1)},#F
    {(0, 2, 0), (0, 1, 0), (0, 1, 1), (-1, 1, 1), (0, 0, 1), (1, 0, 1)},#H
    {(-1, 2, 0), (0, 2, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0), (2, 0, 0)},#I
    {(-1, 2, 1), (-1, 1, 1), (0, 1, 1), (0, 0, 1), (1, 0, 1), (1, 0, 0)},#L

    {(0, 0, 1), (1, 0, 1), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 1, 1)},#O
    {(-1, 1, 1), (0, 1, 1), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, -1, 1)},#P
    {(0, 1, 0), (0, 1, 1), (0, 0, 1), (1, 0, 1), (1, -1, 1), (1, -1, 2)},#S
    {(-1, 1, 1), (0, 1, 1), (0, 0, 1), (1, 0, 1), (1, 0, 0), (1, 1, 0)},#U
    {(-1, 1, 1), (0, 1, 1), (0, 0, 1), (1, 0, 1), (1, 0, 0), (2, 0, 0)},#V
    {(0, 1, 0), (1, 1, 0), (1, 1, -1), (1, 0, 1), (1, 0, 0), (2, 0, 0)},#X
]


hexiamonds = []
origin_x = 100
origin_y = 200
for hex in tri_grid_coords:
    hex_dict = {}
    if origin_x > 900:
        origin_x = 100
        origin_y = 400

    hex_dict['triangles'] = hex
    hex_dict['origin'] = tuple((origin_x, origin_y))
    hex_dict['rotation'] = 0
    hexiamonds.append(hex_dict)
    origin_x += 150

def calculateCoords(hexiamond):
    origin = hexiamond['origin']
    rotation = hexiamond['rotation']
    hexiamond_coordinates = []
    for tri in hexiamond['triangles']:
        cartesian_relative = (tri_corners(tri[0], tri[1], tri[2]))
        hexiamond_coordinates.append(tuple((origin[0] + x, origin[1] - y) for x, y in cartesian_relative)) #position
        #rotation
    return hexiamond_coordinates


pg.init()

# game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('HexiPuzzle')


# Function to check if a point is inside a triangle
def point_in_triangle(pt, triangle):
    def sign(p1, p2, p3):  # pseidoskalarais reizinajums
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    v1, v2, v3 = triangle

    b1 = sign(pt, v1, v2) < 0.0
    b2 = sign(pt, v2, v3) < 0.0
    b3 = sign(pt, v3, v1) < 0.0

    return b1 == b2 == b3

loading_progress = 0
def draw_loading_line():
    pg.draw.line(screen, 'black', (0, 0), (loading_progress, 0), 5)


class DropDown:
    def __init__(self, x, y, w, h, options):
        self.rect = pg.Rect(x, y, w, h)
        self.options = options
        self.selected_option = None
        self.draw_menu = False

    def draw(self, screen, font):
        # Draw the dropdown box
        pg.draw.rect(screen, 'lightgray' if not self.draw_menu else 'gray', self.rect)

        # Draw the selected option or placeholder text
        if self.selected_option is not None:
            text = font.render(self.selected_option, True, 'black')
        else:
            text = font.render("Select Difficulty", True, 'black')
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

        # Draw the dropdown options if the menu is open
        if self.draw_menu:
            for i, option in enumerate(self.options):
                option_rect = pg.Rect(self.rect.x, self.rect.y + self.rect.height + 5 + i * 30, self.rect.width, 30)
                pg.draw.rect(screen, 'lightgray', option_rect)
                option_text = font.render(option, True, 'black')
                option_text_rect = option_text.get_rect(center=option_rect.center)
                screen.blit(option_text, option_text_rect)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu:
                    for i, option in enumerate(self.options):
                        option_rect = pg.Rect(self.rect.x, self.rect.y + self.rect.height + 5 + i * 30, self.rect.width,
                                              30)
                        if option_rect.collidepoint(event.pos):
                            self.selected_option = option
                            self.draw_menu = False

def draw_start_screen():
    screen.fill('burlywood3')
    dropdown = DropDown(400, 400, 200, 30, ["Easy", "Medium", "Hard"])
    start_button_rect = pg.Rect(400, 300, 200, 50)
    pg.draw.rect(screen, 'grey', dropdown)
    pg.draw.rect(screen, 'orange', start_button_rect)
    font = pg.font.Font(None, 36)
    text = font.render("START", True, 'black')
    text_rect = text.get_rect(center=start_button_rect.center)
    screen.blit(text, text_rect)

active_hex = None
hex_colors = ['deeppink', 'darkgoldenrod1', 'purple', 'cyan2', 'darkgreen', 'yellow', 'cornflowerblue',
              'darkorange1', 'lime', 'bisque', 'darkolivegreen4', 'indianred1']
hex_colors_index = 0


def draw_game_screen():
    global hex_colors_index  # Declare hex_colors_index as a global variable
    screen.fill('burlywood3')
    for hex in hexiamonds:
        for tri in calculateCoords(hex):
            pg.draw.polygon(screen, hex_colors[hex_colors_index], tri)
            pg.draw.polygon(screen, 'black', tri, 3)
        hex_colors_index = (hex_colors_index + 1) % len(hex_colors)




current_screen = 'start'


run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if current_screen == 'start':
                    start_button_rect = pg.Rect(400, 300, 200, 50)
                    if start_button_rect.collidepoint(event.pos):
                        current_screen = 'loading'
                elif current_screen == 'game':
                    for num, hex in enumerate(hexiamonds):
                        for tri in calculateCoords(hex):
                            if point_in_triangle(event.pos, tri):
                                active_hex = num
                                break

        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                active_hex = None

        if event.type == pg.MOUSEMOTION:
            if current_screen == 'game' and active_hex is not None:
                dx, dy = event.rel
                current_origin = hexiamonds[active_hex]['origin']
                new_x = max(0, min(current_origin[0] + dx, SCREEN_WIDTH))
                new_y = max(0, min(current_origin[1] + dy, SCREEN_HEIGHT))
                hexiamonds[active_hex]['origin'] = (new_x, new_y)

    if current_screen == 'start':
        draw_start_screen()
    elif current_screen == 'loading':
        draw_loading_line()
        loading_progress += 2
        if loading_progress >= SCREEN_WIDTH:
            current_screen = 'game'
    elif current_screen == 'game':
        draw_game_screen()

    pg.display.flip()

pg.quit()
