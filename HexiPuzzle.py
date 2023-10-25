import pygame
import math
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
    hex_dict['mirror'] = False
    hexiamonds.append(hex_dict)
    origin_x += 150

def calculateCoords(hexiamond):
    origin = hexiamond['origin']
    rotation = hexiamond['rotation']
    mirror = hexiamond['mirror']
    hexiamond_coordinates = []
    for tri in hexiamond['triangles']:
        triangle = tri_corners(tri[0], tri[1], tri[2]) #to cartesian coordinate system
        triangle = rotate(triangle, rotation) #rotating
        if mirror: triangle = (tuple((-x, y)) for x, y in triangle) #mirroring
        triangle = (tuple((origin[0] + x, origin[1] - y) for x, y in triangle)) #positioning
        hexiamond_coordinates.append(triangle)
    return hexiamond_coordinates


pygame.init()

# game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('HexiPuzzle')


# Function to check if a point is inside a hexiamond
def point_in_hex(pt, hex):
    def sign(p1, p2, p3):  # pseidoskalarais reizinajums
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    for tri in hex:
        v1, v2, v3 = tri

        b1 = sign(pt, v1, v2) < 0.0
        b2 = sign(pt, v2, v3) < 0.0
        b3 = sign(pt, v3, v1) < 0.0

        if b1 == b2 == b3:
            return True
    return False

def rotate (tri, rotation):
    angle_radians = math.radians(rotation)
    rotated_tri = []
    for x, y in tri:
        x_new = x * math.cos(angle_radians) + y * math.sin(angle_radians)
        y_new = -x * math.sin(angle_radians) + y * math.cos(angle_radians)
        rotated_tri.append(tuple((x_new, y_new)))
    return rotated_tri


loading_progress = 0
def draw_loading_line():
    pygame.draw.line(screen, 'black', (0, 0), (loading_progress, 0), 5)


def draw_start_screen():
    screen.fill('burlywood3')

    start_button_rect = pygame.Rect(400, 300, 200, 50)
    pygame.draw.rect(screen, 'orange', start_button_rect)
    font = pygame.font.Font(None, 36)
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
            pygame.draw.polygon(screen, hex_colors[hex_colors_index], tri)
            pygame.draw.polygon(screen, 'black', tri, 3)
        hex_colors_index = (hex_colors_index + 1) % len(hex_colors)




current_screen = 'start'

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if current_screen == 'start':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                start_button_rect = pygame.Rect(400, 300, 200, 50)
                if start_button_rect.collidepoint(event.pos):
                    current_screen = 'loading'


        elif current_screen == 'game':

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    indices = list(range(len(hexiamonds)))
                    for num in reversed(indices):
                        hex = hexiamonds[num]
                        if point_in_hex(event.pos, calculateCoords(hex)):
                            active_hex = num
                            break
                if event.button == 3:
                    for hex in reversed(hexiamonds):
                        if point_in_hex(event.pos, calculateCoords(hex)):
                            if hex['mirror']:
                                hex['rotation'] = (hex['rotation'] - 60) % 360
                                break
                            else:
                                hex['rotation'] = (hex['rotation'] + 60) % 360
                                break

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    active_hex = None

            if event.type == pygame.MOUSEMOTION:
                if active_hex is not None:
                    dx, dy = event.rel
                    current_origin = hexiamonds[active_hex]['origin']
                    new_x = max(0, min(current_origin[0] + dx, SCREEN_WIDTH))
                    new_y = max(0, min(current_origin[1] + dy, SCREEN_HEIGHT))
                    hexiamonds[active_hex]['origin'] = (new_x, new_y)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if active_hex is not None:
                    hexiamonds[active_hex]['mirror'] = not hexiamonds[active_hex]['mirror']
                else:
                    for hex in reversed(hexiamonds):
                        if point_in_hex(pygame.mouse.get_pos(), calculateCoords(hex)):
                            hex['mirror'] = not hex['mirror']
                            break

    if current_screen == 'start':
        draw_start_screen()
    if current_screen == 'loading':
        draw_loading_line()
        loading_progress += 2
        if loading_progress >= SCREEN_WIDTH:
            current_screen = 'game'
    elif current_screen == 'game':
        draw_game_screen()

    pygame.display.flip()

pygame.quit()
