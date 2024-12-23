"""
# https://adventofcode.com/2024/day/2
"""
from aocd import get_data

# input = list(get_line_items("aoc_2024/input/02.txt"))
input = get_data(day=2, year=2024).split("\n")

toy_input: list[str] = [
    # fmt: off
    "7 6 4 2 1",
    "1 2 7 8 9",
    "9 7 6 2 1",
    "1 3 2 4 5",
    "8 6 4 4 1",
    "1 3 6 7 9",
    # fmt: on
]


def part_1(input, verbose=False):
    pass


def part_2(input, verbose=False):
    pass


def day_2(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
