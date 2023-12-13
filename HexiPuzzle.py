'''Game rendering and event handler file'''
import pygame
import tkinter as tk
from hexiamonds import *
from puzzleGrids import *
import random

pygame.init()

# game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('HexiPuzzle')


loading_progress = 0

selected_level = "Easy"

grid_1 = None


def draw_loading_line():
    pygame.draw.line(screen, 'black', (0, 0), (loading_progress, 0), 5)



def draw_start_screen(selected_level="Easy"):
    screen.fill('burlywood3')

    # Create and draw start button
    start_button_rect = pygame.Rect(400, 300, 200, 50)
    pygame.draw.rect(screen, 'orange', start_button_rect)
    font = pygame.font.Font(None, 36)
    text = font.render("START", True, 'black')
    text_rect = text.get_rect(center=start_button_rect.center)
    screen.blit(text, text_rect)

    # Return the level buttons from draw_levels
    return draw_levels(selected_level, font)


clock = pygame.time.Clock()
active_hex = None

def draw_levels(selected_level, font=None):
    # Create and draw level buttons in a row
    levels = ["Easy", "Medium", "Hard"]
    level_buttons = []
    button_width, button_height = 150, 50
    gap = 20  # Gap between level buttons
    total_width = len(levels) * (button_width + gap) - gap  # Total width of level buttons

    for i, level in enumerate(levels):
        level_button_rect = pygame.Rect((800 - total_width) // 1.2 + i * (button_width + gap), 400, button_width,
                                        button_height)
        color = 'chartreuse' if level == selected_level else 'azure2'
        pygame.draw.rect(screen, color, level_button_rect)
        level_text = font.render(level, True, 'black')
        level_text_rect = level_text.get_rect(center=level_button_rect.center)
        screen.blit(level_text, level_text_rect)
        level_buttons.append((level, level_button_rect))

    return level_buttons

def draw_game_screen():
    screen.fill('burlywood3')


    # draw grid
    for tri in grid_1.corners:
        pygame.draw.polygon(screen, 'black', tri, 2)

    #draw hexiamonds
    for hex in hexiamonds:
        for tri in hex.get_corners():
            pygame.draw.polygon(screen, hex.color, tri)
            if hex.can_snap(grid_1) and active_hex == hex:
                pygame.draw.polygon(screen, 'white', tri, 2)
            elif hex.can_snap(grid_1):
                pygame.draw.polygon(screen, 'green', tri, 2)
            else:
                pygame.draw.polygon(screen, 'black', tri, 2)


current_screen = 'start'

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        grid_easy = PuzzleGrid(grids_easy[random.randint(0, len(grids_easy) - 1)], (300, 30))
        if current_screen == 'start':
            if selected_level == "Easy":
                grid_1 = grid_easy
            elif selected_level == "Medium":
                grid_1 = grid_medium
            elif selected_level == "Hard":
                grid_1 = grid_hard
            #start button clicked
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                start_button_rect = pygame.Rect(400, 300, 200, 50)
                if start_button_rect.collidepoint(event.pos):
                    loading_progress = 0
                    current_screen = 'loading'
                    # generate_hexiamonds()

                    hexiamonds = []

                    origin_x = 100
                    origin_y = 400
                    for color, hex_tri_grid in zip(hex_colors, hexiamonds_tri_grid):
                        if origin_x > 900:
                            origin_x = 100
                            origin_y = 500
                        hexiamonds.append(Hexiamond(color, hex_tri_grid, origin_x, origin_y))
                        origin_x += 150

                    grid_easy = PuzzleGrid(grids_easy[random.randint(0, len(grids_easy) - 1)], (300, 30))
                    grid_medium = PuzzleGrid(grids_medium[random.randint(0, len(grids_medium) - 1)], (300, 30))
                    grid_hard = PuzzleGrid(grids_hard[random.randint(0, len(grids_hard) - 1)], (300, 30))

                for level, button_rect in draw_start_screen(selected_level):
                    if button_rect.collidepoint(event.pos):
                        selected_level = level
                        grid_easy = PuzzleGrid(grids_easy[random.randint(0, len(grids_easy) - 1)], (300, 30))
                        grid_medium = PuzzleGrid(grids_medium[random.randint(0, len(grids_medium) - 1)], (300, 30))
                        grid_hard = PuzzleGrid(grids_hard[random.randint(0, len(grids_hard) - 1)], (300, 30))
                        current_screen = 'start'
                        draw_start_screen(selected_level)
        elif current_screen == 'game':

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(mouse_pos):
                    # Add functionality to go back to the previous page
                    current_screen = 'start'
                    draw_start_screen(selected_level)
                #hexiamond picked up with cursor
                if event.button == 1:
                    for hex in reversed(hexiamonds):
                        if hex.point_in(event.pos):
                            active_hex = hex
                            hexiamonds.remove(active_hex)
                            hexiamonds.append(active_hex) #move to top
                            hex.remove_from_grid(grid_1)
                            break

                #hexiamond is rotated
                if event.button == 3:
                    for hex in reversed(hexiamonds):
                        if hex.point_in(event.pos):
                            if hex.mirror:
                                hex.rotation = (hex.rotation - 1) % 6
                            else:
                                hex.rotation = (hex.rotation + 1) % 6
                            hex.remove_from_grid(grid_1)
                            hex.snap(grid_1)
                            break
            #hexiamond is dropped
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if active_hex:
                        active_hex.snap(grid_1)
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
                if active_hex:
                    active_hex.mirror = not active_hex.mirror
                else:
                    for hex in reversed(hexiamonds):
                        if hex.point_in(pygame.mouse.get_pos()):
                            hex.mirror = not hex.mirror
                            hex.remove_from_grid(grid_1)
                            hex.snap(grid_1)
                            break

    if current_screen == 'start':
        draw_start_screen(selected_level)
        # font = pygame.font.Font(None, 36)
        # draw_levels(selected_level, font)


    if current_screen == 'loading':
        draw_loading_line()
        loading_progress += 2
        if loading_progress >= SCREEN_WIDTH:
            current_screen = 'game'
    elif current_screen == 'game':
        draw_game_screen()

        level_font = pygame.font.Font(None, 36)
        level_text = level_font.render(f'Selected level: {selected_level}', True, 'black')  # Use level_font here
        screen.blit(level_text, (20, 20))

        white = (255, 255, 255)
        black = (0, 0, 0)

        # Font for the back button
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        back_button_rect = pygame.Rect(60, 60, 100, 40)
        pygame.draw.rect(screen, white, back_button_rect)  # Draw the back button background
        back_button_text = font.render("Back", True, black)  # Define back_button_text here
        screen.blit(back_button_text, (60, 60))

        fps = clock.get_fps()
        font = pygame.font.Font(None, 36)
        fps_text = font.render(f'FPS: {int(fps)}', True, 'black')
        screen.blit(fps_text, (10, 10))
        clock.tick()

    pygame.display.flip()


pygame.quit()
