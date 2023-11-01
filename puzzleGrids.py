'''Puzzle grid generation and helper functions'''
from grids.src.updown_tri import *

grids_simple = [
    [
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0)
    ]
]

class PuzzleGrid:
    def __init__(self, grid_simple):
        self.triangles = convert_grid(grid_simple)
        self.fill = None

    def to_cartesian(self, origin):
        grid_coordinates = []
        for tri in self.triangles:
            triangle = (tri_corners(tri[0], tri[1], tri[2]))
            triangle = (tuple((origin[0] + x, origin[1] - y) for x, y in triangle))  # positioning
            grid_coordinates.append(triangle)
        return grid_coordinates


# returns triangle on the right of given
def moveRight(a, b, c):
    if points_up(a, b, c):
        return (a, b, c - 1)
    else:
        return (a + 1, b, c)

# returns triangle below given
def moveDown(a, b, c):
    if points_up(a, b, c):
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



grid_1 = PuzzleGrid(grids_simple[0])
# print(grid_1.triangles)