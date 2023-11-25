"""
# https://adventofcode.com/2022/day/8
"""
import pytest

from aoc_2022.days.day08 import (
    input,
    toy_input,
    part_1,
    part_2,
    build_vis_grid,
    calc_view_distances,
    count_visible,
    scenic_score,
    two_d_array_from_digit_strings,
    Coord,
    VisGrid,
)


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


@pytest.mark.parametrize("coord,expected", [[(1, 2), 4], [(3, 2), 8]])
def test_score(coord: Coord, expected: int, toy_grid):
    distances = calc_view_distances(coord, toy_grid)
    assert scenic_score(distances) == expected


def test_part_1_toy():
    assert part_1(toy_input) == 21


def test_part_1_real():
    assert part_1(input) == 1845


def test_part_2_toy():
    assert part_2(toy_input) == 8


def test_part_2_real():
    assert part_2(input) == 230112
