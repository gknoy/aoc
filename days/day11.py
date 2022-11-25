"""
# Dumbo Octopus
# https://adventofcode.com/2021/day/11
"""
from copy import deepcopy
from typing import List, Set, Tuple, Union
from utils import Coord, Grid, get_line_items, two_d_array_from_digit_strings, neighbors
from colors import bold, none

input = list(get_line_items("input/11.txt"))
toy_input: List[str] = [
    "5483143223",
    "2745854711",
    "5264556173",
    "6141336146",
    "6357385478",
    "4167524645",
    "2176841721",
    "6882881134",
    "4846848554",
    "5283751526",
]
# toy_input = [
#     "11111",
#     "19991",
#     "19191",
#     "19991",
#     "11111",
# ]


class NicerGrid:
    """A 2d array that can be a"""

    def __init__(self, data):
        self.data = deepcopy(data)
        self.n_rows = len(data)
        self.n_cols = len(data[0])
        self.max_row = self.n_rows - 1
        self.max_col = self.n_cols - 1
        self.coords = [
            (row, col) for row in range(self.n_rows) for col in range(self.n_cols)
        ]

    def __getitem__(self, index: Union[int, Coord]) -> int:
        """
        Let is do grid[coord], e.g. grid[(3, 4)] instead of having to deconstruct them all the time
        """
        if type(index) is int:
            return self.data[index]
        if type(index) is tuple and len(index) == 2:
            return self.data[index[0]][index[1]]
        raise IndexError

    def __setitem__(self, index: Union[int, Coord], value):
        """
        Let is do grid[coord], e.g. grid[(3, 4)] instead of having to deconstruct them all the time
        """
        if type(index) is tuple and len(index) == 2:
            self.data[index[0]][index[1]] = value
            return self.data[index[0]][index[1]]

    def __str__(self):
        """Render grid with bold zeros"""
        grid = self.data

        def render_cell(row: int, col: int) -> str:
            number = grid[row][col]
            n_str = f"{number:1}"
            return bold(n_str) if number == 0 else n_str

        grid_rows = self.n_rows
        grid_cols = self.n_cols
        row_strings = [
            "".join(
                [render_cell(row_index, col_index) for col_index in range(grid_cols)]
            )
            for row_index in range(grid_rows)
        ]
        return "\n".join(row_strings)


def flash(neighbor: Coord, grid: NicerGrid, flashed: Set[Coord]) -> int:
    # print(f" --- flash {neighbor}")
    # if neighbor in flashed:
    #     # this one already flashed once
    #     print(f"    ({neighbor} already flashed)")
    flash_count = 0
    if neighbor not in flashed:
        flash_count = 1
        flashed.add(neighbor)
        for neighbor in neighbors(neighbor, grid.max_row, grid.max_col):
            grid[neighbor] += 1
            if neighbor not in flashed and grid[neighbor] > 9:
                flash_count += flash(neighbor, grid, flashed)

    return flash_count


#
# - First, the energy level of each octopus increases by 1.
# - Then, any octopus with an energy level greater than 9 flashes.
# - This increases the energy level of all adjacent octopuses by 1,
#   including octopuses that are diagonally adjacent.
# - If this causes an octopus to have an energy level greater than 9, it also flashes.
# - This process continues as long as new octopuses keep having their energy level increased beyond 9.
# - (An octopus can only flash at most once per step.)
# - Finally, any octopus that flashed during this step has its energy level set to 0
#
def step(grid: NicerGrid, verbose=False):
    flashed = set()
    # increase all energy levels by one
    if verbose:
        print(">>> increase all by one")
    for coord in grid.coords:
        grid[coord] += 1

    # flash each octopus with energy > 9
    gt_nines = {c for c in grid.coords if grid[c] > 9}
    if verbose:
        print(f">>> GT 9: {gt_nines}")

    flash_count = sum(flash(coord, grid, flashed) for coord in gt_nines)

    if verbose:
        print(f">>> flashed {flashed}")
    for coord in flashed:
        if grid[coord] > 9:
            if verbose:
                print(f"--- zeroing {coord}")
            grid[coord] = 0

    if verbose:
        print(grid)

    return flash_count


def part_1(input, verbose=False):
    """
    How many total flashes are there after 100 steps?
    """
    grid = NicerGrid(two_d_array_from_digit_strings(input))

    return sum(step(grid, verbose=verbose) for i in range(100))


def part_2(input, verbose=False):
    grid = NicerGrid(two_d_array_from_digit_strings(input))
    grid_size = grid.n_rows * grid.n_cols

    step_number = 0
    while True:
        step_number += 1
        n_flashed = step(grid, verbose=verbose)
        if n_flashed == grid_size:
            # and {0} == set(grid[coord] for coord in grid.coords):
            return step_number


def day_11(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
