'''Game rendering and event handler file'''
import pygame
from hexiamonds import *
from puzzleGrids import *

pygame.init()

# game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('HexiPuzzle')



loading_progress = 0
def draw_loading_line():
    pygame.draw.line(screen, 'black', (0, 0), (loading_progress, 0), 5)

def draw_start_screen():
    screen.fill('burlywood3')

    #create and draw start button
    start_button_rect = pygame.Rect(400, 300, 200, 50)
    pygame.draw.rect(screen, 'orange', start_button_rect)
    font = pygame.font.Font(None, 36)
    text = font.render("START", True, 'black')
    text_rect = text.get_rect(center=start_button_rect.center)
    screen.blit(text, text_rect)

active_hex = None


def draw_game_screen():
    global hex_colors_index
    screen.fill('burlywood3')

    # draw grid
    for tri in grid_1.to_cartesian((300, 50)):
        pygame.draw.polygon(screen, 'black', tri, 3)

    #draw hexiamonds
    for hex in hexiamonds:
        for tri in hex.to_cartesian():
            pygame.draw.polygon(screen, hex.color, tri)
            pygame.draw.polygon(screen, 'black', tri, 3)


current_screen = 'start'

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if current_screen == 'start':
            #start button clicked
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                start_button_rect = pygame.Rect(400, 300, 200, 50)
                if start_button_rect.collidepoint(event.pos):
                    current_screen = 'loading'


        elif current_screen == 'game':

            if event.type == pygame.MOUSEBUTTONDOWN:
                #hexiamond picked up with cursor
                if event.button == 1:
                    for hex in reversed(hexiamonds):
                        if hex.point_in(event.pos):
                            active_hex = hex
                            hexiamonds.remove(active_hex)
                            hexiamonds.append(active_hex)
                            break

                #hexiamond is rotated
                if event.button == 3:
                    for hex in reversed(hexiamonds):
                        if hex.point_in(event.pos):
                            if hex.mirror:
                                hex.rotation = (hex.rotation - 1) % 6
                                break
                            else:
                                hex.rotation = (hex.rotation + 1) % 6
                                break
            #hexiamond is dropped
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # if (active_hex):
                    #     active_hex.snap()
                    active_hex = None

            #hexiamond is dragged
            if event.type == pygame.MOUSEMOTION:
                if active_hex is not None:
                    dx, dy = event.rel
                    current_origin = active_hex.origin
                    new_x = max(0, min(current_origin[0] + dx, SCREEN_WIDTH))
                    new_y = max(0, min(current_origin[1] + dy, SCREEN_HEIGHT))
                    active_hex.origin = (new_x, new_y)

            #hexiamond is mirrored
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if active_hex is not None:
                    active_hex.mirror = not active_hex.mirror
                else:
                    for hex in reversed(hexiamonds):
                        if hex.point_in(pygame.mouse.get_pos()):
                            hex.mirror = not hex.mirror
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
