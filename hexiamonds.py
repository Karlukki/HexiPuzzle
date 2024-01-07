'''Hexiamond generation, transformations and helper functions '''
import math
import pygame
from puzzleGrids import *
from tkinter import messagebox
from grids.src.updown_tri import *



hex_colors = ['deeppink', 'darkgoldenrod1', 'purple', 'cyan2', 'darkgreen', 'yellow', 'cornflowerblue',
              'darkorange1', 'lime', 'bisque', 'darkolivegreen4', 'indianred1']

# Hexiamonds in triangular grid representation
hexiamonds_tri_grid = [
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
class Hexiamond:
    '''Data structure and methods for hexiamonds(puzzle pieces)'''
    def __init__(self, color, hex_tri_grid, origin_x, origin_y):
        self.color = color
        self.initial_origin = tuple((origin_x, origin_y))
        self.triangles = hex_tri_grid
        self.origin = tuple((origin_x, origin_y))
        self.rotation = 0
        self.mirror = False


    def get_corners(self):
        '''Hexiamond transformations and conversion to cartesian coordinates'''
        origin = self.origin
        rotation = self.rotation
        mirror = self.mirror
        hexiamond_coordinates = set()
        for tri in self.triangles:
            triangle = tri_rotate_60(tri[0], tri[1], tri[2], -rotation)  # rotation
            if mirror: triangle = tri_reflect_x(triangle[0], triangle[1], triangle[2])  # mirorring
            triangle = tri_corners(triangle[0], triangle[1], triangle[2])  # conversion to cartesian coordinates
            triangle = tuple((origin[0] + x, origin[1] - y) for x, y in triangle) # positioning
            hexiamond_coordinates.add(triangle)
        return hexiamond_coordinates


    def get_centers(self, origin=None):
        '''Returns set of triangle center coordinates if the hexiamond were located at given origin'''
        if origin is None:
            origin = self.origin
        rotation = self.rotation
        mirror = self.mirror
        hexiamond_coordinates = set()
        for tri in self.triangles:
            triangle = tri_rotate_60(tri[0], tri[1], tri[2], -rotation)  # rotation
            if mirror: triangle = tri_reflect_x(triangle[0], triangle[1], triangle[2])  # mirorring
            center = tri_center(triangle[0], triangle[1], triangle[2])  # conversion to cartesian coordinates
            center = (origin[0] + center[0], origin[1] - center[1])  # positioning
            hexiamond_coordinates.add(center)
        return hexiamond_coordinates


    def point_in(self, pt):
        '''Returns if a point is inside self'''
        def sign(p1, p2, p3):  # pseidoskalarais reizinajums
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        for tri in self.get_corners():
            v1, v2, v3 = tri

            b1 = sign(pt, v1, v2) < 0.0
            b2 = sign(pt, v2, v3) < 0.0
            b3 = sign(pt, v3, v1) < 0.0

            if b1 == b2 == b3:
                return True
        return False


    def can_snap(self, grid):
        '''If hexiamond can snap to grid, returns the point and the tris that would be filled, else returns None'''
        # gets the closest crosspoint
        closest = None
        min_distance = float('inf')
        for point in grid.crosspoints:
            dist = distance(point, self.origin)
            if dist < min_distance:
                min_distance = dist
                closest = point

        # if the hexiamond were moved to closest crosspoint, would it fit?
        free_tris = grid.free_tris()
        tris_with_centers_inside = list()

        for center in self.get_centers(closest):
            inside_cell = False
            for tri in free_tris:
                if point_in_tri(tri, center):
                    inside_cell = True
                    tris_with_centers_inside.append(tri)
                    break
            if not inside_cell: #snapping not possible
                return None

        return closest, tris_with_centers_inside
    def snap(self, grid, message = True):
        '''Snaps (attaches) hexiamond to grid'''
        if self.can_snap(grid):
            self.origin = self.can_snap(grid)[0]
            for tri in self.can_snap(grid)[1]:
                tri['color'] = self.color
            if message and grid.free_tris() == list():
                # Display congrats
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                pygame.event.set_blocked(pygame.KEYDOWN)
                messagebox.showinfo("Congratulations!", "You solved the puzzle!")
                pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                pygame.event.set_allowed(pygame.KEYDOWN)

    def is_snapped_to(self, grid):
        '''Returns if hexiamond is snapped (attached) to grid'''
        for tri in grid.triangles:
            if tri['color'] == self.color:
                return True
        return False

    def detach_from_grid(self, grid):
        '''Detaches hexiamond from grid'''
        for tri in grid.triangles:
            if tri['color'] == self.color:
                tri['color'] = None

    def reset_location(self):
        '''Resets origin and rotation of hexiamond to initial values'''
        self.origin = self.initial_origin
        self.rotation = 0


def distance(point1, point2):
    '''Returns distance between 2 points'''
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


#generates list of hexiamonds
hexiamonds = []

origin_x = 100
origin_y = 400
for color, hex_tri_grid in zip(hex_colors, hexiamonds_tri_grid):
    if origin_x > 900:
        origin_x = 100
        origin_y = 500
    hexiamonds.append(Hexiamond(color, hex_tri_grid, origin_x, origin_y))
    origin_x += 150
