"""
# https://adventofcode.com/2024/day/1
"""
from aocd import get_data

from utils.utils import get_line_items

# input = list(get_line_items("aoc_2024/input/01.txt"))
input = get_data(day=1, year=2024)

toy_input: list[str] = [
    # fmt: off
    # fmt: on
]


def part_1(input, verbose=False):
    pass


def part_2(input, verbose=False):
    pass


def day_1(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
