"""
# https://adventofcode.com/2021/day/9
"""
from typing import Optional, Set, Tuple
from utils import BOLD, CLEAR, get_line_items, two_d_array_from_digt_strings

input = list(get_line_items("input/09.txt"))
toy_input = [
    # lines input
    "2199943210",
    "3987894921",
    "9856789892",
    "8767896789",
    "9899965678",
]


def render(grid, bolded_coords: Optional[Set[Tuple[int, int]]] = None):
    """
    Print a 2d grid with some coordinates bolded

    :param grid:
    :param bolded_coords:
    :return:
    """
    bolded_coords = bolded_coords or set()

    def render_cell(row: int, col: int) -> str:
        number = grid[row][col]
        if (row, col) in bolded_coords:
            return f"{BOLD}{number:1}{CLEAR}"
        return f"{number:1}"

    grid_rows = len(grid)
    grid_cols = len(grid[0])
    row_strings = [
        "".join([render_cell(row_index, col_index) for col_index in range(grid_cols)])
        for row_index in range(grid_rows)
    ]
    return "\n".join(row_strings)


def find_local_minima(grid):
    """Get the set of grid coordinates that are local minima"""
    min_row = min_col = 0
    max_row = len(grid) - 1
    max_col = len(grid[0]) - 1

    def is_minima(row, col):
        # cell value is smaller than all its neighbors

        # fmt: off
        return (
                (row == min_row or grid[row][col] < grid[row - 1][col])
            and (row == max_row or grid[row][col] < grid[row + 1][col])
            and (col == min_col or grid[row][col] < grid[row][col - 1])
            and (col == max_col or grid[row][col] < grid[row][col + 1])
        )
        # fmt: on

    # Look at every cell
    return set(
        (row, col)
        for row in range(len(grid))
        for col in range(len(grid[row]))
        if is_minima(row, col)
    )


def part_1(input, verbose=False):
    grid = two_d_array_from_digt_strings(input)

    local_minima = find_local_minima(grid)

    if verbose:
        print(render(grid, bolded_coords=local_minima))

    def risk(coord):
        # The risk level of a low point is 1 plus its height"
        row, col = coord
        return 1 + grid[row][col]

    return sum(map(risk, local_minima))


def part_2(input, verbose=False):
    pass


def day_9(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
