import pygame
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


pygame.init()

# game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('HexiPuzzle')


# Function to check if a point is inside a triangle
def point_in_triangle(pt, triangle):
    def sign(p1, p2, p3):  # pseidoskalarais reizinajums
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    v1, v2, v3 = triangle

    b1 = sign(pt, v1, v2) < 0.0
    b2 = sign(pt, v2, v3) < 0.0
    b3 = sign(pt, v3, v1) < 0.0

    return b1 == b2 == b3

active_hex = None
hex_colors = ['deeppink', 'darkgoldenrod1', 'purple', 'cyan2', 'darkgreen', 'yellow', 'cornflowerblue', 'darkorange1', 'lime', 'bisque', 'darkolivegreen4', 'indianred1']
hex_colors_index = 0

run = True
while run:
    screen.fill('black')
    for hex in hexiamonds:
        for tri in calculateCoords(hex):
            if hex_colors_index > 11:
                hex_colors_index = 0

            pygame.draw.polygon(screen, hex_colors[hex_colors_index], tri)
            pygame.draw.polygon(screen, 'white', tri, 3)
        hex_colors_index += 1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, hex in enumerate(hexiamonds):
                    for tri in calculateCoords(hex):
                        if point_in_triangle(event.pos, tri):
                            active_hex = num
                            break

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_hex = None

        if event.type == pygame.MOUSEMOTION:
            if active_hex != None:
                dx, dy = event.rel
                current_origin = hexiamonds[active_hex]['origin']
                new_origin = (current_origin[0] + dx, current_origin[1] + dy)
                hexiamonds[active_hex]['origin'] = new_origin


    pygame.display.flip()

pygame.quit()
