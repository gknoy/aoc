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
    """
    Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
    """
    best = 0
    current = []

    for item in input:
        if item == "":
            current_sum = sum(current)
            if current_sum > best:
                best = current_sum
            if verbose:
                print(f">>> {best} -- {current_sum} <-- {current}")
            current = []
            continue
        val = int(item)
        current.append(val)

    # handle the last item if there is one ;)
    if len(current):
        current_sum = sum(current)
        if current_sum > best:
            best = current_sum
        if verbose:
            print(f">>> {best} -- {current_sum} <-- {current}")

    return best


def part_2(input, verbose=False):
    pass


def day_1(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
