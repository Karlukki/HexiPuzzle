import pygame
from grids.src.updown_tri import *

hexiamond = {(0, 0, 1), (1, 0, 1), (1, 0, 0), (2, 0, 0), (0, 0, 2), (1, 1, 0)}


def getHexiamondCoordinates(hexiamond, origin_x, origin_y):
    hexiamond_coordinates = []
    for triangle in hexiamond:
        cartesian_relative = (tri_corners(triangle[0], triangle[1], triangle[2]))
        hexiamond_coordinates.append(tuple((x + origin_x, -y + origin_y) for x, y in cartesian_relative))
    return hexiamond_coordinates


hexiamond_cartesian = getHexiamondCoordinates(hexiamond, 300, 300)

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


run = True
while run:
    screen.fill('white')
    for triangle in hexiamond_cartesian:
        pygame.draw.polygon(screen, 'red', triangle)
        pygame.draw.polygon(screen, 'black', triangle, 3)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         if event.button == 1:
    #             for num, tri in enumerate(triangles):
    #                 if point_in_triangle(event.pos, tri):
    #                     active_tri = num
    #
    #     if event.type == pygame.MOUSEBUTTONUP:
    #         if event.button == 1:
    #             active_tri = None
    #
    #     if event.type == pygame.MOUSEMOTION:
    #         if active_tri != None:
    #             dx, dy = event.rel
    #             triangles[active_tri] = [(x + dx, y + dy) for x, y in triangles[active_tri]]
    #

    # if (active_tri is not None):
    #     pygame.draw.polygon(screen, 'red', triangles[active_tri])
    #
    pygame.display.flip()

pygame.quit()
