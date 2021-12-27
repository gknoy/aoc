"""
# https://adventofcode.com/2021/day/9
"""
from typing import Callable, Dict, Optional, Set, Tuple
from colors import none, bold, cyan, red, green, blue, magenta, yellow

from utils import get_line_items, neighbors, two_d_array_from_digt_strings

input = list(get_line_items("input/09.txt"))
toy_input = [
    # lines input
    "2199943210",
    "3987894921",
    "9856789892",
    "8767896789",
    "9899965678",
]


def render(grid, color_coords: Optional[Dict[Callable, Set[Tuple[int, int]]]] = None):
    """Print a 2d grid with some coordinates in colors"""
    color_coords = color_coords or {}

    def render_cell(row: int, col: int) -> str:
        number = grid[row][col]
        for color_fn, coords in color_coords.items():
            if (row, col) in coords:
                return color_fn(f"{number:1}")
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


# --------------------------
# Part 1: Find minima
# --------------------------


def part_1(input, verbose=False):
    grid = two_d_array_from_digt_strings(input)

    local_minima = find_local_minima(grid)

    if verbose:
        print(">>> Part 1 Minima:")
        print(render(grid, {bold: local_minima}))

    def risk(coord):
        # The risk level of a low point is 1 plus its height"
        row, col = coord
        return 1 + grid[row][col]

    return sum(map(risk, local_minima))


# --------------------------
# Part 2: Find basins
# --------------------------


def test_coord_manipulations():
    c = (3, 5)
    expected = {"up": (2, 5), "down": (4, 5), "left": (3, 4), "right": (3, 6)}
    vals = {"up": up(c), "down": down(c, 9), "left": left(c), "right": right(c, 9)}
    assert expected == vals

    c = (9, 9)
    expected = {"up": (8, 9), "down": c, "left": (9, 8), "right": c}
    vals = {"up": up(c), "down": down(c, 9), "left": left(c), "right": right(c, 9)}
    assert expected == vals

    c = (0, 0)
    expected = {"up": c, "down": (1, 0), "left": c, "right": (0, 1)}
    vals = {"up": up(c), "down": down(c, 9), "left": left(c), "right": right(c, 9)}
    assert expected == vals


def fill_basin(grid, starting_minimum: Tuple[int, int]) -> Set[Tuple[int, int]]:
    # expand until we are no longer going uphill, or encounter a Nine
    basin = {starting_minimum}
    max_row = len(grid) - 1
    max_col = len(grid[0]) - 1

    def _grid(coord):
        return grid[coord[0]][coord[1]]

    queue = [starting_minimum]
    while len(queue):
        # print(f"\n Q: {queue}")
        item = queue.pop(0)
        # print(f"  item: {item}")

        current_val = _grid(item)
        # nbcs = neighbors(item, max_row, max_col)
        # print(f" -- neighbors: {nbcs}")
        for coord in neighbors(item, max_row, max_col, include_diagonals=False):
            # print(f"neighbor: {coord}")
            val = _grid(coord)
            # print(f"  cur: {current_val} < {val} ?")
            if val < 9 and val >= current_val and coord not in basin:
                # print(f"  Adding {coord} to basin")
                basin.add(coord)
                queue.append(coord)

    # print(f"basin: {basin}")
    return basin


def colorize_items(items):
    # assign colors
    # TODO: Use color constants instead of functions
    #       so that we can use gradient scaling for pretty rendering
    # colors = ["cyan", "red", "green", "blue", "magenta", "yellow"]
    colors = [cyan, red, green, blue, magenta, yellow]
    n_colors = len(colors)
    return [(colors[index % n_colors], item) for index, item in enumerate(items)]


def combine_dicts_of_sets(kv_pairs):
    # keys are colors, which are not unique since we have more regions than
    # colors in the map
    d = {}
    for k, vals in kv_pairs:
        if k not in d:
            d[k] = set()
        d[k] = d[k] | vals
    return d


def part_2(input, verbose=False):
    """
    A basin is all locations that eventually flow downward to a single low point.
    Therefore, every low point has a basin, although some basins are very small.
    Locations of height 9 do not count as being in any basin, and
    all other locations will always be part of exactly one basin.

    The size of a basin is the number of locations within the basin, including the low point. The example above has four basins.

    The top-left basin, size 3:

    2199943210
    3987894921
    9856789892
    8767896789
    9899965678
    """
    grid = two_d_array_from_digt_strings(input)

    if verbose:
        print("--- Day 9 Part 2 ---")

    local_minima = find_local_minima(grid)

    if verbose:
        print(f"Local minima: {local_minima}")

    nines = set(
        (row, col)
        for row in range(len(grid))
        for col in range(len(grid[row]))
        if grid[row][col] == 9
    )

    # sets of coords
    basins = [fill_basin(grid, minimum) for minimum in local_minima]
    basin_sizes = list(reversed(sorted(len(basin) for basin in basins)))

    score = 1
    for size in basin_sizes[:3]:
        score *= size

    if verbose:
        # (color_fn, coords) tuples
        # colors are NOT unique so we can't make a dict directly
        colorized_basins = combine_dicts_of_sets(colorize_items(basins))
        color_coords = {**colorized_basins, none: local_minima, bold: nines}
        print(">>> Part 2 basins:")
        # TODO: render height gradient with shading of any given color
        print(render(grid, color_coords=color_coords))
        print(f"Top three basins:\n  {basin_sizes[:3]} -> {score}")

    return score


def day_9(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
