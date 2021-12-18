"""
# https://adventofcode.com/2021/day/9
"""
from utils import get_line_items

input = list(get_line_items("input/09.txt"))
toy_input = [
    "2199943210",
    "3987894921",
    "9856789892",
    "8767896789",
    "9899965678",
]


def part_1(input, verbose=False):
    pass


def part_2(input, verbose=False):
    pass


def day_9(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
