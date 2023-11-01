'''Hexiamond generation, transformations and helper functions '''
from grids.src.updown_tri import *

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
    def __init__(self, hex_tri_grid, origin_x, origin_y):
        self.triangles = hex_tri_grid
        self.origin = tuple((origin_x, origin_y))
        self.rotation = 0
        self.mirror = False



    # Hexiamond transformations and conversion to cartesian coordinates
    def to_cartesian(self):
        origin = self.origin
        rotation = self.rotation
        mirror = self.mirror
        hexiamond_coordinates = set()
        for tri in self.triangles:
            triangle = tri_rotate_60(tri[0], tri[1], tri[2], -rotation)  # rotation
            if mirror: triangle = tri_reflect_x(triangle[0], triangle[1], triangle[2])  # mirorring
            triangle = tri_corners(triangle[0], triangle[1], triangle[2])  # conversion to cartesian coordinates
            triangle = (tuple((origin[0] + x, origin[1] - y) for x, y in triangle))  # positioning
            hexiamond_coordinates.add(triangle)
        return hexiamond_coordinates


    # Function to check if a point is inside a hexiamond
    def point_in(self, pt):
        def sign(p1, p2, p3):  # pseidoskalarais reizinajums
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        for tri in self.to_cartesian():
            v1, v2, v3 = tri

            b1 = sign(pt, v1, v2) < 0.0
            b2 = sign(pt, v2, v3) < 0.0
            b3 = sign(pt, v3, v1) < 0.0

            if b1 == b2 == b3:
                return True
        return False

# generates a list of all hexiamonds
hexiamonds = []
origin_x = 100
origin_y = 200
for hex_tri_grid in hexiamonds_tri_grid:
    if origin_x > 900:
        origin_x = 100
        origin_y = 400
    hexiamonds.append(Hexiamond(hex_tri_grid, origin_x, origin_y))
    origin_x += 150
