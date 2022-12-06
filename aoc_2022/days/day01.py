"""
# https://adventofcode.com/2022/day/1
"""
from typing import List
from utils.utils import get_line_items

input = list(get_line_items("aoc_2022/input/01.txt"))
toy_input: List[str] = [
    "1000",
    "2000",
    "3000",
    "",
    "4000",
    "",
    "5000",
    "6000",
    "",
    "7000",
    "8000",
    "9000",
    "",
    "10000",
]


def part_1(input, verbose=False):
    pass


def part_2(input, verbose=False):
    pass


def day_1(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
