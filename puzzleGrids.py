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
    def __init__(self, grid_simple, game_origin, select_origin):
        self.game_origin = game_origin
        self.select_origin = select_origin
        self.simple = grid_simple
        self.triangles = self.get_triangles()
        self.crosspoints = self.get_crosspoints()

    def get_triangles(self):
        triangles = convert_grid(self.simple)
        triangleslist = list()
        for tri in triangles:
            tri_info = dict()
            tri_info['tri'] = tri
            tri_info['game_corners'] = get_corners(tri, self.game_origin)
            updown_tri.edge_length = 30
            tri_info['select_corners'] = get_corners(tri, self.select_origin)
            updown_tri.edge_length = 45
            tri_info['color'] = None
            triangleslist.append(tri_info)
        return triangleslist


    def get_crosspoints(self):
        crosspoints = set()
        for tri in self.triangles:
            crosspoints.update(tri['game_corners'])
        return crosspoints


    #function checks if a point is inside self
    def point_in(self, pt, size):
        def sign(p1, p2, p3):  # pseidoskalarais reizinajums
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        for tri in self.triangles:
            v1, v2, v3 = tri[size]

            b1 = sign(pt, v1, v2) < 0.0
            b2 = sign(pt, v2, v3) < 0.0
            b3 = sign(pt, v3, v1) < 0.0

            if b1 == b2 == b3:
                return True
        return False

    def free_tris(self):
        return [tri for tri in self.triangles if tri['color'] is None]


def get_corners(tri, origin):
    corners = (updown_tri.tri_corners(tri[0], tri[1], tri[2]))
    corners = (tuple((origin[0] + x, origin[1] - y) for x, y in corners))  # positioning
    return corners

# checks if point is in given cell (corners given)
def point_in_tri(tri, pt):
    def sign(p1, p2, p3):  # pseidoskalarais reizinajums
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    v1, v2, v3 = tri['game_corners']

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


x_left = 100
x_right = 900
width = 200

grids = {}
for key, value in grids_simple.items():
    gap = (x_right - x_left - width*len(value)) / (len(value)+1)
    grids[key] = [PuzzleGrid(grid, (300, 30), (x_left + (i+1)*gap + i*width, 250)) for i, grid in enumerate(value)]



