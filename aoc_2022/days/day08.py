"""
# https://adventofcode.com/2022/day/8
"""
from functools import reduce
from typing import Callable, List
from utils.utils import (
    get_line_items,
    two_d_array_from_digit_strings,
    vertical_slice,
    grid_at,
    Coord,
    Grid,
    up,
    down,
    left,
    right,
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


# ----------------------------
# Viewing Distance
# ----------------------------


def view_distance(
    coord: Coord, grid: Grid, direction: Callable, max_or_min_in_direction: int
) -> int:
    # if we are on an edge
    count = 0
    height = grid_at(grid, coord)
    prev_coord = coord
    next_coord = direction(coord, max_or_min_in_direction)
    # print(f">>> view_distance({coord}, {direction})")
    while next_coord != prev_coord:
        # print(f"    next: {next_coord}")
        # we are not on an edge, so we can see at least one tree:
        count += 1
        if grid_at(grid, next_coord) >= height:
            return count
        prev_coord = next_coord
        next_coord = direction(
            next_coord, max_or_min_in_direction
        )  # keep going in same direction
    # if we reach the edge, then we're done in this direction
    return count


def calc_view_distances(coord: Coord, grid: Grid) -> List[int]:
    max_col = len(grid) - 1
    max_row = len(grid[0]) - 1
    return [
        view_distance(coord, grid, up, 0),
        view_distance(coord, grid, down, max_row),
        view_distance(coord, grid, left, 0),
        view_distance(coord, grid, right, max_col),
    ]


def scenic_score(distances: List[int]) -> int:
    return reduce(lambda a, b: a * b, distances)


def part_2(input, verbose=False):
    """
    Consider each tree on your map. What is the highest scenic score possible for any tree?

    Viewing distance:
        stop if you reach an edge
        or at the first tree that is the same height or taller than the tree under consideration.
    Scenic score: multiply viewing distance in each direction
    """
    grid = two_d_array_from_digit_strings(input)
    max_score = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            coord = (row, col)
            score = scenic_score(calc_view_distances(coord, grid))
            if score > max_score:
                max_score = score
    return max_score


def day_8(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
