"""
# Day 3: Binary Diagnostic
#
# https://adventofcode.com/2021/day/3
"""
from utils import get_line_items

toy_data = [
    "00100",
    "11110",
    "10110",
    "10111",
    "10101",
    "01111",
    "00111",
    "11100",
    "10000",
    "11001",
    "00010",
    "01010",
]

data = [item for item in get_line_items("input/03.txt")]


def part_1(data):
    return None


def part_2(data):
    return None


def day_3(use_toy_data=False):
    _data = toy_data if use_toy_data else data
    return [part_1(_data), part_2(_data)]
