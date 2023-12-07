"""
# https://adventofcode.com/2023/day/2
"""
from utils.utils import get_line_items

input = list(get_line_items("aoc_2023/input/02.txt"))
toy_input: list[str] = [
    # fmt: off
    # fmt: on
]


def part_1(input, verbose=False):
    pass


def part_2(input, verbose=False):
    pass


def day_2(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
