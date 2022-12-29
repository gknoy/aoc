"""
# https://adventofcode.com/2022/day/8
"""
from typing import List
from utils.utils import get_line_items

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


def part_1(input, verbose=False):
    pass


def part_2(input, verbose=False):
    pass


def day_8(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
