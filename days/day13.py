"""
# https://adventofcode.com/2021/day/13
"""
from typing import List
from utils import get_line_items

input = list(get_line_items("input/13.txt"))
toy_input: List[str] = [
    "6,10",
    "0,14",
    "9,10",
    "0,3",
    "10,4",
    "4,11",
    "6,0",
    "6,12",
    "4,1",
    "0,13",
    "10,12",
    "3,4",
    "3,0",
    "8,4",
    "1,10",
    "2,14",
    "8,10",
    "9,0",
    "",
    "fold along y=7",
    "fold along x=5",
]


def part_1(input, verbose=False):
    """
    How many dots are visible after completing just the first fold
    instruction on your transparent paper?
    """
    pass


def part_2(input, verbose=False):
    pass


def day_13(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
