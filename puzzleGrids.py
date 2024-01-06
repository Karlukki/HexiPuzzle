'''Puzzle grid generation and helper functions'''
from grids.src.updown_tri import *
import grids.src.updown_tri as updown_tri
import random

# grids_simple = [
#         (0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),
#         (0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0),
#         (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
#         (0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
#         (0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
#         (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
#         (0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0),
#         (0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),
#     ]

grids_simple = dict()
grids_simple['easy'] = [
    [
        (1, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1),
    ],
    [
        (0, 1, 1, 1, 1, 1, 1, 1, 1, 1),
        (0, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    ],
]
grids_simple['medium'] = [
    [
        (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
        (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
        (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ]
]
grids_simple['hard'] = [
    [
        (0,0,0,0,0,0,1,0,0,0,0,0),
        (0,0,0,0,0,1,1,1,0,0,0,0),
        (0,1,1,1,1,1,1,1,1,1,1,1),
        (0,0,1,1,1,1,1,1,1,1,1,0),
        (0,0,1,1,1,1,1,1,1,1,1,0),
        (0,1,1,1,1,1,1,1,1,1,1,1),
        (0,0,0,0,0,1,1,1,0,0,0,0),
        (0,0,0,0,0,0,1,0,0,0,0,0),
    ],
    [
        (0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0),
        (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0),
        (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
        (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
        (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
        (0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
        (0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0),
    ]
]


class PuzzleGrid:
    def __init__(self, grid_simple, origin):
        self.origin = origin
        self.simple = grid_simple
        self.triangles = convert_grid(grid_simple)
        self.corners = self.get_corners()
        self.crosspoints = self.get_crosspoints()

    def get_corners(self):
        origin = self.origin
        grid_coordinates = dict()
        for tri in self.triangles:
            corners = (updown_tri.tri_corners(tri[0], tri[1], tri[2]))
            corners = (tuple((origin[0] + x, origin[1] - y) for x, y in corners))  # positioning
            grid_coordinates[corners] = None
        return grid_coordinates

    def get_crosspoints(self):
        corners = self.corners
        crosspoints = set()
        for tri in corners:
            crosspoints.update(tri)
        return crosspoints


    #function checks if a point is inside self
    def point_in(self, pt):
        def sign(p1, p2, p3):  # pseidoskalarais reizinajums
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        for tri in self.corners:
            v1, v2, v3 = tri

            b1 = sign(pt, v1, v2) < 0.0
            b2 = sign(pt, v2, v3) < 0.0
            b3 = sign(pt, v3, v1) < 0.0

            if b1 == b2 == b3:
                return True
        return False

    def free_cells(self):
        return {key for key, value in self.corners.items() if value is None}

# checks if point is in given cell (corners given)
def point_in_cell(cell, pt):
    def sign(p1, p2, p3):  # pseidoskalarais reizinajums
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    v1, v2, v3 = cell

    b1 = sign(pt, v1, v2) < 0.0
    b2 = sign(pt, v2, v3) < 0.0
    b3 = sign(pt, v3, v1) < 0.0

    if b1 == b2 == b3:
        return True
    return False


# returns triangle on the right of given
def moveRight(a, b, c):
    if updown_tri.points_up(a, b, c):
        return (a, b, c - 1)
    else:
        return (a + 1, b, c)

# returns triangle below given
def moveDown(a, b, c):
    if updown_tri.points_up(a, b, c):
        return (a, b - 1, c)
    else:
        return (a + 1, b - 1, c + 1)


# converts grid in simple representation to tri_grid representation
def convert_grid(grid_simple):
    grid = set()
    first_of_row = (1, 0, 1)
    current_tri = first_of_row
    for row in grid_simple:
        for current_tri_bool in row:
            if current_tri_bool == 1:
                grid.add(current_tri)
            current_tri = moveRight(current_tri[0], current_tri[1], current_tri[2])
        first_of_row = moveDown(first_of_row[0], first_of_row[1], first_of_row[2])
        current_tri = first_of_row
    return grid


# game_grids = {key: [PuzzleGrid(grid, (300, 30)) for grid in value] for key, value in grids_simple.items()}

updown_tri.edge_length = 30
x_left = 100
x_right = 900
width = 200

select_grids = {}
for key, value in grids_simple.items():
    gap = (x_right - x_left - width*len(value)) / (len(value)+1)
    select_grids[key] = [PuzzleGrid(grid, (x_left + (i+1)*gap + i*width, 250)) for i, grid in enumerate(value)]

updown_tri.edge_length = 45

