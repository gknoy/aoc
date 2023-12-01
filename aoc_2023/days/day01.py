"""
# https://adventofcode.com/2023/day/1
"""
from utils.utils import get_line_items

input = list(get_line_items("aoc_2023/input/01.txt"))
toy_input: list[str] = [
    # fmt: off
    "1abc2",
    "pqr3stu8vwx",
    "a1b2c3d4e5f",
    "treb7uchet",
    # fmt: on
]


def part_1(input, verbose=False):
    pass


def part_2(input, verbose=False):
    pass


def day_1(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
