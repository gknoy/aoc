"""
# https://adventofcode.com/2021/day/7
"""
from utils import get_line_items

input = list(get_line_items("input/07.txt"))
toy_input = ["16,1,2,0,4,2,7,1,2,14"]


def part_1(input, verbose=False):
    pass


def part_2(input, verbose=False):
    pass


def day_7(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
