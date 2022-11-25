"""
# https://adventofcode.com/2021/day/14
"""
from typing import List
from utils import get_line_items

input = list(get_line_items("input/14.txt"))
toy_input: List[str] = [
    "NNCB",  # starting polymer
    "",
    "CH -> B",  # insertion rules
    "HH -> N",
    "CB -> H",
    "NH -> C",
    "HB -> C",
    "HC -> B",
    "HN -> C",
    "NN -> C",
    "BH -> H",
    "NC -> B",
    "NB -> B",
    "BN -> B",
    "BB -> N",
    "BC -> B",
    "CC -> N",
    "CN -> C",
]


def part_1(input, verbose=False):
    """
    Apply 10 steps of pair insertion to the polymer template and
    find the most and least common elements in the result.
    What do you get if you take the quantity of the most common element and
    subtract the quantity of the least common element?
    """
    pass


def part_2(input, verbose=False):
    pass


def day_14(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
