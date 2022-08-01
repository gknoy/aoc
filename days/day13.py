"""
# https://adventofcode.com/2021/day/13
"""
import numpy as np
from numpy.typing import ArrayLike, NDArray
from pprint import pprint
from typing import Dict, List, Tuple
from utils import get_line_items

input = list(get_line_items("input/13.txt"))
toy_input: List[str] = [
    # x,y => col, row
    "6,10",
    "0,14",
    "9,10",
    "0,3",
    "10,4",
    "4,11",
    "6,0",
    "6,12",
    "4,1",
    "0,13",
    "10,12",
    "3,4",
    "3,0",
    "8,4",
    "1,10",
    "2,14",
    "8,10",
    "9,0",
    "",
    "fold along y=7",
    "fold along x=5",
]


def parse_marks_and_instructions(input: List[str]) -> Tuple[List[List[int]], List]:
    mark_positions = []
    instructions = []
    for line in input:
        if "," in line:
            row, col = map(int, line.split(","))
            # store
            mark_positions.append([row, col])
        if "fold" in line:
            instruction = line.replace("fold along", "")
            instruction = instruction.split("=")
            instructions.append(instruction)
    return mark_positions, instructions


def create_np_grid(marks: List[List[int]]) -> ArrayLike:
    # the grid is a grid of booleans, but numpy lets us treat them as zero and 1
    max_rows = 1 + max(mark[1] for mark in marks)
    max_cols = 1 + max(mark[0] for mark in marks)
    print(f">>> max_rows: {max_rows}")
    print(f">>> max_cols: {max_cols}")
    grid = np.zeros([max_rows, max_cols], bool)
    for col, row in marks:
        grid[row][col] = True
    return grid


class Paper:
    def __init__(self, grid: ArrayLike):
        self.grid = grid
        self.rendered = None

    def fold(self, direction: str, index: int):
        if direction == "x":
            self.fold_x(index)
        if direction == "y":
            self.fold_y(index)
        raise Exception(f"Invalid direction: {direction}")

    def fold_x(self, col: int) -> ArrayLike:
        """
        ..#.               ..|#.      .#
        .##.  fold_x(2) -> .#|#.  ->  .#
        #...               #.|..      #.
        """
        raise NotImplemented

    def fold_y(self, row: int) -> ArrayLike:
        """
        ..#.               ..#.      #.#.
        .##.  fold_y(2) -> .##.  ->  ###.
        #...               ----
        #...               #...
                           #...
        """
        raise NotImplemented

    # --- debugging aids :)
    def render_row(self, grid_row):
        return "".join(["#" if item else "." for item in grid_row])

    def render(self):
        if self.rendered is not None:
            return self.rendered
        self.rendered = "\n".join(self.render_row(row) for row in self.grid)
        return self.rendered

    def __eq__(self, other):
        if type(other) == Paper:
            # np.array == np.array generates a comparison array
            return (
                len(self.grid) == len(other.grid)
                and len(self.grid[0]) == len(other.grid[0])
                and (self.grid == other.grid).all()
            )
        if type(other) == str:
            return self.render() == other
        return False

    def print(self):
        print(self.render())


def part_1(input, verbose=False):
    """
    How many dots are visible after completing just the first fold
    instruction on your transparent paper?
    """
    marks, instructions = parse_marks_and_instructions(input)
    if verbose:
        print(">>> marks:")
        pprint(marks)
    grid = create_np_grid(marks)

    paper = Paper(grid)
    if verbose:
        print(f">>> starting paper:\n{paper.render()}")
    pass


def part_2(input, verbose=False):
    pass


def day_13(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
