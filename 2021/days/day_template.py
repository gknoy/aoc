"""
# https://adventofcode.com/2021/day/N
"""
from typing import List
from utils import get_line_items

input = list(get_line_items("input/NN.txt"))
toy_input: List[str] = []


def part_1(input, verbose=False):
    pass


def part_2(input, verbose=False):
    pass


def day_N(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
