import pygame
import random

pygame.init()

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Drag And Drop')

active_tri = None
triangles = []
base_length = 50
height = 40
for i in range(5):
    x1, y1 = random.randint(50, 700), random.randint(50, 350)
    base_length = 50
    height = 40

    x2, y2 = x1 + base_length, y1
    x3, y3 = x1 + base_length / 2, y1 - height

    triangles.append([(x1, y1), (x2, y2), (x3, y3)])

print(triangles)

# Function to check if a point is inside a triangle
def point_in_triangle(pt, triangle):

    def sign(p1, p2, p3): # pseidoskalarais reizinajums
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    v1, v2, v3 = triangle

    b1 = sign(pt, v1, v2) < 0.0
    b2 = sign(pt, v2, v3) < 0.0
    b3 = sign(pt, v3, v1) < 0.0

    return b1 == b2 == b3


run = True
while run:
    screen.fill('black')


    # Draw triangles
    for triangle in triangles:
        pygame.draw.polygon(screen, 'red', triangle)


    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, tri in enumerate(triangles):
                    if point_in_triangle(event.pos, tri):
                        active_tri = num

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_tri = None

        if event.type == pygame.MOUSEMOTION:
            if active_tri != None:
                dx, dy = event.rel
                triangles[active_tri] = [(x + dx, y + dy) for x, y in triangles[active_tri]]

        if event.type == pygame.QUIT:
            run = False

    if (active_tri is not None):
        pygame.draw.polygon(screen, 'red', triangles[active_tri])

    pygame.display.flip()

pygame.quit()