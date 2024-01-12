'''Game rendering and event handler file'''
import pygame
import tkinter as tk
from hexiamonds import *
from puzzleGrids import *
import json

pygame.init()

# game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('HexiPuzzle')

selected_difficulty = 'easy'
difficulty_buttons = list()

game_grid = None
active_hex = None
clock = pygame.time.Clock()


def save_progress():
    with open('progressdata.txt', 'w') as file:
        progressdata[str(game_grid.simple)] = {}
        progressdata[str(game_grid.simple)]['colors'] = {str(tri['tri']): tri['color'] for tri in game_grid.triangles if
                                                         tri['color'] is not None}
        progressdata[str(game_grid.simple)]['hexiamonds'] = {
            hex.color: {'origin': hex.origin, 'rotation': hex.rotation, 'mirror': hex.mirror} for hex in hexiamonds if
            hex.is_snapped_to(game_grid)}
        json.dump(progressdata, file)

def make_diff_buttons():
    global difficulty_buttons, selected_difficulty
    difficulty_buttons = []

    difficulties = grids.keys()
    button_width, button_height = 150, 50
    gap = 20
    total_width = len(difficulties) * (button_width + gap) - gap

    for i, diff in enumerate(difficulties):
        button_rect = pygame.Rect((800 - total_width) // 1.2 + i * (button_width + gap), 400, button_width, button_height)
        color = 'chartreuse' if diff == selected_difficulty else 'azure2'
        font = pygame.font.Font(None, 36)
        text = font.render(diff, True, 'black')
        text_rect = text.get_rect(center=button_rect.center)

        difficulty_buttons.append({'diff': diff, 'color': color, 'text': text, 'button_rect': button_rect, 'text_rect': text_rect})

make_diff_buttons()


font = pygame.font.Font(pygame.font.get_default_font(), 36)
back_button_rect = pygame.Rect(60, 60, 100, 40)
back_button_text = font.render("Back", True, 'black')

def draw_back_button():
    global back_button_rect, back_button_text
    pygame.draw.rect(screen, 'white', back_button_rect)
    screen.blit(back_button_text, (60, 60))

    diff_font = pygame.font.Font(None, 36)
    diff_text = diff_font.render(f'Difficulty: {selected_difficulty}', True, 'black')
    screen.blit(diff_text, (20, 20))


font = pygame.font.Font(pygame.font.get_default_font(), 18)
reset_all_button_rect = pygame.Rect(800, 20, 165, 22)
reset_all_button_text = font.render("Reset all progress", True, 'black')

def draw_start_screen():
    screen.fill('burlywood3')
    #draw difficulty buttons
    for button in difficulty_buttons:
        pygame.draw.rect(screen, button['color'], button['button_rect'])
        screen.blit(button['text'], button['text_rect'])

    #draw start button
    start_button_rect = pygame.Rect(400, 300, 200, 50)
    pygame.draw.rect(screen, 'orange', start_button_rect)
    font = pygame.font.Font(None, 36)
    text = font.render("START", True, 'black')
    text_rect = text.get_rect(center=start_button_rect.center)
    screen.blit(text, text_rect)

    #draw reset all progress button
    pygame.draw.rect(screen, 'white', reset_all_button_rect)
    screen.blit(reset_all_button_text, (800, 20))

    #draw level completion text
    completed_easy = 1  # Update this value based on the actual completion status
    completed_medium = 2
    completed_hard = 3

    text_box_rect = pygame.Rect(300, 500, 50, 10)  # Adjust the coordinates and size
    pygame.draw.rect(screen, 'burlywood3', text_box_rect)
    font = pygame.font.Font(None, 36)
    completion_text = font.render(f"{completed_easy}/3", True, 'black')
    completion_text_rect = completion_text.get_rect(center=text_box_rect.center)
    screen.blit(completion_text, completion_text_rect)

    text_box_rect = pygame.Rect(470, 500, 50, 10)  # Adjust the coordinates and size
    pygame.draw.rect(screen, 'burlywood3', text_box_rect)
    font = pygame.font.Font(None, 36)
    completion_text = font.render(f"{completed_medium}/3", True, 'black')
    completion_text_rect = completion_text.get_rect(center=text_box_rect.center)
    screen.blit(completion_text, completion_text_rect)

    text_box_rect = pygame.Rect(650, 500, 50, 10)  # Adjust the coordinates and size
    pygame.draw.rect(screen, 'burlywood3', text_box_rect)
    font = pygame.font.Font(None, 36)
    completion_text = font.render(f"{completed_hard}/3", True, 'black')
    completion_text_rect = completion_text.get_rect(center=text_box_rect.center)
    screen.blit(completion_text, completion_text_rect)



def draw_grid_select():
    screen.fill('burlywood3')
    with open('progressdata.txt', 'r') as file:
        progressdata = json.load(file)
        for grid in grids[selected_difficulty]:
            for tri in grid.triangles:
                if str(grid.simple) in progressdata and str(tri['tri']) in progressdata[str(grid.simple)]['colors']:
                    color = progressdata[str(grid.simple)]['colors'][str(tri['tri'])]
                    pygame.draw.polygon(screen, color, tri['select_corners'])
                else:
                    pygame.draw.polygon(screen, 'burlywood4', tri['select_corners'])
                if grid.point_in(pygame.mouse.get_pos(), 'select_corners'):
                    pygame.draw.polygon(screen, 'white', tri['select_corners'], 2)
                else:
                    pygame.draw.polygon(screen, 'black', tri['select_corners'], 2)


font = pygame.font.Font(pygame.font.get_default_font(), 18)
reset_button_rect = pygame.Rect(830, 20, 145, 22)
reset_button_text = font.render("Reset Progress", True, 'black')

clean_button_rect = pygame.Rect(730, 20, 85, 22)
clean_button_text = font.render("Clean up", True, 'black')


def draw_game_screen():
    screen.fill('burlywood3')

    #draw game grid
    for tri in game_grid.triangles:
        pygame.draw.polygon(screen, 'burlywood4', tri['game_corners'])
        pygame.draw.polygon(screen, 'black', tri['game_corners'], 2)

    #draw hexiamonds
    for hex in hexiamonds:
        for tri in hex.get_corners():
            pygame.draw.polygon(screen, hex.color, tri)
            if hex.can_snap(game_grid) and active_hex == hex:
                pygame.draw.polygon(screen, 'white', tri, 2)
            elif hex.can_snap(game_grid):
                pygame.draw.polygon(screen, 'green', tri, 2)
            else:
                pygame.draw.polygon(screen, 'black', tri, 2)

    #draw reset buttton
    pygame.draw.rect(screen, 'white', reset_button_rect)
    screen.blit(reset_button_text, (830, 20))

    #draw clean up buttton
    pygame.draw.rect(screen, 'white', clean_button_rect)
    screen.blit(clean_button_text, (730, 20))

    draw_controls()

def draw_controls():
    image_width, image_height = 50, 50
    margin = 830
    current_y = 55

    controls_info = [
        {"image": "space.png", "purpose": 'Mirror'},
        {"image": "lmb.png", "purpose": 'Drag'},
        {"image": "rmb.png", "purpose": 'Rotate'},
    ]

    for control_info in controls_info:
        image_path = control_info["image"]
        purpose = control_info["purpose"]

        try:
            control_image = pygame.image.load(image_path)
            control_image = pygame.transform.scale(control_image, (image_width, image_height))
            image_rect = control_image.get_rect(topleft=(margin, current_y))
            screen.blit(control_image, image_rect)
        except pygame.error as e:
            print(f"Error loading image {image_path}: {e}")

        font = pygame.font.Font(None, 24)
        text = font.render(purpose, True, 'black')
        text_rect = text.get_rect(topleft=(margin + image_width + 10, current_y + (image_height - text.get_height()) // 2))
        screen.blit(text, text_rect)

        current_y += 60


current_screen = 'start'

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if current_screen == 'start':

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #difficulty button clicked
                for button in difficulty_buttons:
                    if button['button_rect'].collidepoint(event.pos):
                        selected_difficulty = button['diff']
                        make_diff_buttons()

                #start button clicked
                start_button_rect = pygame.Rect(400, 300, 200, 50)
                if start_button_rect.collidepoint(event.pos):
                    current_screen = 'grid_select'

                #reset all progress button clicked
                if reset_all_button_rect.collidepoint(event.pos):
                    if game_grid:
                        [hex.detach_from_grid(game_grid) for hex in hexiamonds]
                    with open('progressdata.txt', 'w') as file:
                        json.dump({}, file)
                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                    messagebox.showinfo("Success!", "All your progress has been reset!")
                    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)


        elif current_screen == 'grid_select':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #back button to start
                if back_button_rect.collidepoint(event.pos):
                    current_screen = 'start'

                #grid is selected
                for grid in grids[selected_difficulty]:
                    if grid.point_in(event.pos, 'select_corners'):
                        game_grid = grid

                        with open('progressdata.txt', 'r') as file:
                            progressdata = json.load(file)
                            for hex in hexiamonds:
                                if str(game_grid.simple) in progressdata and hex.color in progressdata[str(game_grid.simple)]['hexiamonds']:
                                    hex.origin = tuple(progressdata[str(game_grid.simple)]['hexiamonds'][hex.color]['origin'])
                                    hex.rotation = progressdata[str(game_grid.simple)]['hexiamonds'][hex.color]['rotation']
                                    hex.mirror = progressdata[str(game_grid.simple)]['hexiamonds'][hex.color]['mirror']
                                else:
                                    hex.reset_location()

                        [hex.snap(game_grid, False) for hex in hexiamonds]
                        current_screen = 'game'

        elif current_screen == 'game':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # back button to grid select
                    if back_button_rect.collidepoint(event.pos):
                        save_progress()
                        current_screen = 'grid_select'

                    #reset progress is clicked
                    if reset_button_rect.collidepoint(event.pos):
                        for hex in hexiamonds:
                            hex.detach_from_grid(game_grid)
                            hex.reset_location()

                    #clean up is clicked
                    if clean_button_rect.collidepoint(event.pos):
                        for hex in hexiamonds:
                            if not hex.is_snapped_to(game_grid):
                                hex.detach_from_grid(game_grid)
                                hex.reset_location()

                    #hexiamond picked up with cursor
                    for hex in reversed(hexiamonds):
                        if hex.point_in(event.pos):
                            active_hex = hex
                            hexiamonds.remove(active_hex)
                            hexiamonds.append(active_hex) #move to top
                            hex.detach_from_grid(game_grid)
                            [hex.snap(game_grid) for hex in hexiamonds if hex != active_hex]
                            break

                #hexiamond is rotated
                if event.button == 3:
                    for hex in reversed(hexiamonds):
                        if hex.point_in(event.pos):
                            if hex.mirror:
                                hex.rotation = (hex.rotation - 1) % 6
                            else:
                                hex.rotation = (hex.rotation + 1) % 6
                            hex.detach_from_grid(game_grid)
                            hex.snap(game_grid)
                            break
            #hexiamond is dropped
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if active_hex:
                        active_hex.snap(game_grid)
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
                            hex.detach_from_grid(game_grid)
                            hex.snap(game_grid)
                            break

    if current_screen == 'start':
        draw_start_screen()

    elif current_screen == 'grid_select':
        draw_grid_select()
        draw_back_button()
    elif current_screen == 'game':
        draw_game_screen()
        draw_back_button()


        fps = clock.get_fps()
        font = pygame.font.Font(None, 36)
        fps_text = font.render(f'FPS: {int(fps)}', True, 'black')
        screen.blit(fps_text, (5, 575))
        clock.tick()

    pygame.display.flip()


if current_screen == 'game':
    save_progress()
pygame.quit()
