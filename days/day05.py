"""
# https://adventofcode.com/2021/day/5
"""
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


def part_1(input, verbose=False):
    pass


def part_2(input, verbose=False):
    pass


def day_5(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
