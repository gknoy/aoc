"""
# Dumbo Octopus
# https://adventofcode.com/2021/day/11
"""
from typing import List
from utils import get_line_items, two_d_array_from_digt_strings

input = list(get_line_items("input/11.txt"))
toy_input: List[str] = [
    "5483143223",
    "2745854711",
    "5264556173",
    "6141336146",
    "6357385478",
    "4167524645",
    "2176841721",
    "6882881134",
    "4846848554",
    "5283751526",
]


def part_1(input, verbose=False):
    grid = two_d_array_from_digt_strings(input)
    pass


def part_2(input, verbose=False):
    pass


def day_11(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
