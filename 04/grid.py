"""
This is a copy of the grid library I used in 2024.  I'm interested to see if I
can get through 2025 without making any changes.
"""

from collections import namedtuple
from functools import cache
import math
from typing import Iterable


class Vector(namedtuple("Vector", ["i", "j"])):
    """
    2D vector.  Since we're usually coming from an ascii grid, we'll say i is
    the row and j  is the column.   0,0 would be the upper left, or the very
    first character.
    """

    @classmethod
    def dot(cls, a: "Vector", b: "Vector") -> int:
        return a.i * b.i + a.j * b.j

    def __add__(self, other: "Vector") -> "Vector":
        # Could almost certainly optimize this
        return get_vector(self.i + other.i, self.j + other.j)

    def __sub__(self, other: "Vector") -> "Vector":
        return get_vector(self.i - other.i, self.j - other.j)

    def __mul__(self, other: int) -> "Vector":
        """
        Scalar multiplication, not dot product.
        """
        return get_vector(self.i * other, self.j * other)

    def __div__(self, other: int) -> "Vector":
        """
        Scalar division
        """
        return get_vector(self.i / other, self.j / other)

    def __abs__(self) -> float:
        """Magnitude"""
        return math.sqrt(self.i ** 2 + self.j ** 2)

    def unit(self) -> "Vector":
        return get_vector(self.i / abs(self), self.j / abs(self))


@cache
def get_vector(i: int, j: int) -> Vector:
    return Vector(i, j)


NORTH = get_vector(-1, 0)
NORTH_EAST = get_vector(-1, 1)
EAST = get_vector(0, 1)
SOUTH_EAST = get_vector(1, 1)
SOUTH = get_vector(1, 0)
SOUTH_WEST = get_vector(1, -1)
WEST = get_vector(0, -1)
NORTH_WEST = get_vector(-1, -1)

CARDINAL_DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

ALL_DIRECTION_VECTORS = [
    NORTH,
    NORTH_EAST,
    EAST,
    SOUTH_EAST,
    SOUTH,
    SOUTH_WEST,
    WEST,
    NORTH_WEST,
]

def turn_90(direction:Vector, clockwise:int) -> Vector:
    return CARDINAL_DIRECTIONS[(CARDINAL_DIRECTIONS.index(direction) + 1 * clockwise) % 4]

def turn_left(direction:Vector) -> Vector:
    return turn_90(direction, -1)

def turn_right(direction:Vector) -> Vector:
    return turn_90(direction, 1)


class Grid:
    """
    2D Grid. Not sure this shouldn't just be defaultdict like I usually do.
    """

    def __init__(self, out_of_bounds="."):
        self.grid = {}
        self.out_of_bounds = out_of_bounds

    def __getitem__(self, key: Vector):
        return self.grid.get(key, self.out_of_bounds)

    def __setitem__(self, key: Vector, value):
        self.grid[key] = value

    def all_locations(self) -> Iterable[Vector]:
        return self.grid.keys()

    def find(self, value) -> Iterable[Vector]:
        return (location for location, cell in self.grid.items() if cell == value)

    def find_one(self, value) -> Vector:
        found_locations = list(self.find(value))
        if len(found_locations) != 1:
            print(found_locations)
            raise Exception("Expected to find one location")
        return found_locations[0]


def grid_from_input_txt(ascii_grid: str, out_of_bounds=".") -> Grid:
    """
    Import an ascii grid into a Grid object
    """
    grid = Grid(out_of_bounds)
    for i, row in enumerate(ascii_grid.split("\n")):
        for j, cell in enumerate(row):
            grid.grid[get_vector(i, j)] = cell
    return grid

def print_grid(grid:Grid):
    """
    Print a grid.  This is a little more complicated than it could be because
    we have to find the bounds of the grid.
    """
    min_i = min_j = max_i = max_j = 0
    for location in grid.all_locations():
        max_i = max(max_i, location.i)
        max_j = max(max_j, location.j)

    for i in range(min_i, max_i + 1):
        for j in range(min_j, max_j + 1):
            print(grid[get_vector(i, j)], end="")
        print()
