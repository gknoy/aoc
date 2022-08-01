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
            instruction = line.replace("fold along ", "")
            instruction = instruction.split("=")
            instructions.append(instruction)
    return mark_positions, instructions


def create_np_grid(marks: List[List[int]]) -> ArrayLike:
    # A grid of booleans would be more efficiency
    max_rows = 1 + max(mark[1] for mark in marks)
    max_cols = 1 + max(mark[0] for mark in marks)
    # print(f">>> max_rows: {max_rows}")
    # print(f">>> max_cols: {max_cols}")
    grid = np.zeros([max_rows, max_cols], np.int8)
    for col, row in marks:
        grid[row][col] = 1
    return grid


class Paper:
    def __init__(self, grid: ArrayLike):
        self.grid = grid
        self.rendered = None

    def fold(self, direction: str, index: int):
        if direction == "x":
            return self.fold_x(index)
        if direction == "y":
            return self.fold_y(index)
        raise Exception(f"Invalid direction: >>{direction}<<")

    def fold_x(self, col: int):
        """
        ...#.               ..|#.      .#
        .#.#.  fold_x(2) -> .#|#.  ->  .#
        #....               #.|..      #.
        """
        print(f">>> fold_x {col}")
        # left, right = self.partition_x(col)
        raise Exception(f"fold_x({col}) not implemented")

    def fold_y(self, row: int):
        """
        ..#.               ..#.      #.#.
        .##.  fold_y(2) -> .##.  ->  ###.
        ....               ----  (line is ignored)
        #...               #...
        #...               #...
        """
        top = np.array(self.grid[:row])
        # the row'th row is ignored in the fold
        bottom = self.grid[row + 1 :]
        flipped_bottom = np.array([row for row in reversed(bottom)])
        self.rendered = None
        self.grid = np.array(top | flipped_bottom)

    def __repr__(self):
        return self.render()

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

    def count_marks(self) -> int:
        return self.grid.sum()

    def print(self):
        print(self.render())


def part_1(input, verbose=False):
    """
    How many dots are visible after completing just the first fold
    instruction on your transparent paper?
    """
    marks, instructions = parse_marks_and_instructions(input)
    # if verbose:
    #     print(">>> marks:")
    #     pprint(marks)
    grid = create_np_grid(marks)

    paper = Paper(grid)
    if verbose:
        print(f">>> starting paper:\n{paper.render()}")

    axis, index = instructions[0]
    folded = paper.fold(axis, index)


def part_2(input, verbose=False):
    pass


def day_13(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]


# debugging aids
marks, instructions = parse_marks_and_instructions(toy_input)
grid = create_np_grid(marks)
paper = Paper(grid)
