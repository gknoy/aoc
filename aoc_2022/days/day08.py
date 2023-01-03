"""
# https://adventofcode.com/2022/day/8
"""
import pytest
from typing import List
from utils.utils import (
    get_line_items,
    two_d_array_from_digit_strings,
    vertical_slice,
    Grid,
)

input = list(get_line_items("aoc_2022/input/08.txt"))
toy_input: List[str] = [
    # fmt: off
    "30373",
    "25512",
    "65332",
    "33549",
    "35390",
    # fmt: on
]

# -------------------------
# Calculating visibility
# -------------------------
#
# Left/Right Visibility in a row:
#
#     112213110140442401434531255323512525265655352543623565556265545555235551143135124203142220020302000
#
#     y.y..y....y..........y...............y............................................................. from left
#     ..........................................................y..................y.......y.......y.y..y from right
#
# Items in a row can be visible from top/bottom, as well
#
# Naiive scan is O(n^2):  O(3*rows*cols)
# (2x rows, 2x cols, + row*col to traverse the grid)
# Real input is 107 x 1000
#

VisGrid = List[List[bool]]
VisRow = List[bool]
GridRow = List[int]


def calc_visibility_row(grid_row: GridRow) -> VisRow:
    n_cols = len(grid_row)
    vis = [False for _ in range(n_cols)]
    # leftmost + rightmost are definitely visible
    vis[0] = True
    vis[-1] = True
    # scan from left and right at same time
    tallest_from_west = grid_row[0]
    tallest_from_east = grid_row[-1]
    west_index = 0
    east_index = n_cols - 1
    tallest_west_index = west_index
    tallest_east_index = east_index
    while west_index <= tallest_east_index and east_index >= tallest_west_index:
        if grid_row[west_index] > tallest_from_west:
            vis[west_index] = True
            tallest_from_west = grid_row[west_index]
            tallest_west_index = west_index
        if grid_row[east_index] > tallest_from_east:
            vis[east_index] = True
            tallest_from_east = grid_row[east_index]
            tallest_east_index = east_index
        west_index += 1
        east_index -= 1
    return vis


def build_vis_grid_rows(grid: Grid) -> VisGrid:
    """
    Generate the initial visibility grid for a given grid size
    """
    return [calc_visibility_row(row) for row in grid]


def set_vis_grid_cols(grid: Grid, vis_grid: VisGrid):
    n_cols = len(grid[0])
    # first and last cols are already visible from the row calcs:
    for col_index in range(1, n_cols - 1):
        vis_col: VisRow = vertical_slice(grid, col_index)
        for row, visible in enumerate(calc_visibility_row(vis_col)):
            if visible:
                vis_grid[row][col_index] = True


def build_vis_grid(grid: Grid) -> VisGrid:
    vis = build_vis_grid_rows(grid)
    set_vis_grid_cols(grid, vis)
    return vis


def count_visible(vis_grid: VisGrid) -> int:
    # FIXME: for large grids, this is less efficient than counting while
    #        doing the visibility calcs
    return sum(sum(1 for item in row if item) for row in vis_grid)


# ----------------------------
# tests
# ----------------------------


@pytest.fixture
def toy_grid():
    """
    30373
    25512
    65332
    33549
    35390
    """
    return two_d_array_from_digit_strings(toy_input)


def test_calc_vis(toy_grid):
    expected = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1],
    ]
    expected_vis: VisGrid = [[col == 1 for col in row] for row in expected]
    vis_grid = build_vis_grid(toy_grid)
    assert vis_grid == expected_vis
    vis_count = count_visible(vis_grid)
    assert vis_count == sum(sum(row) for row in expected)


def part_1(input, verbose=False):
    """
    With 16 trees visible on the edge and another 5 visible in the interior,
    a total of 21 trees are visible in this arrangement.

    Consider your map; how many trees are visible from outside the grid?
    """
    grid = two_d_array_from_digit_strings(input)
    vis_grid = build_vis_grid(grid)
    n_visible = count_visible(vis_grid)
    return n_visible


def part_2(input, verbose=False):
    pass


def day_8(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
