"""
# https://adventofcode.com/2021/day/5
"""
import pytest
from utils import get_line_items

input = list(get_line_items("input/05.txt"))
toy_input = [
    "0,9 -> 5,9",
    "8,0 -> 0,8",
    "9,4 -> 3,4",
    "2,2 -> 2,1",
    "7,0 -> 7,4",
    "6,4 -> 2,0",
    "0,9 -> 2,9",
    "3,4 -> 1,4",
    "0,0 -> 8,8",
    "5,5 -> 8,2",
]

expected_maps = {
    1: """.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....""",
    2: None,
}


def parse_input(lines):
    # return pairs of tuples for each line
    return [[tuple(pair.split(",")) for pair in line.split(" -> ")] for line in lines]


def interpolate(a, b):
    # Get all the points on a line between a and b,
    # accounting for slope between a and b
    delta_x = b[0] - a[0]
    delta_y = b[1] - a[1]
    slope = delta_y / delta_x  # this can be negative
    # b can be leftward of a:
    step = 1 if (a[0] < b[0]) else -1

    def f(x):
        # point on line (segment) intersecting A and B
        return a[1] + slope * (x - a[0])

    return [(x, f(x)) for x in range(a[0], b[0] + step, step)]


@pytest.mark.parametrize(
    "a,b,expected",
    [
        [(0, 0), (2, 2), [(0, 0), (1, 1), (2, 2)]],
        [(2, 2), (0, 0), [(0, 0), (1, 1), (2, 2)]],
        [(0, 2), (2, 0), [(0, 2), (1, 1), (2, 0)]],
        [(2, 0), (0, 2), [(0, 2), (1, 1), (2, 0)]],
    ],
)
def test_interpolate(a, b, expected):
    assert sorted(interpolate(a, b)) == expected


def init_grid():
    # FIXME: Use sparse grid in numpy
    return []


def part_1(input, verbose=False):
    pass


def part_2(input, verbose=False):
    pass


def day_5(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    data = parse_input(data)
    return [part_1(data, verbose), part_2(data, verbose)]
