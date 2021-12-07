"""
# https://adventofcode.com/2021/day/7
"""
from math import ceil, floor
from statistics import median

from utils import get_line_items, parse_one_line_input

input = list(get_line_items("input/07.txt"))
toy_input = ["16,1,2,0,4,2,7,1,2,14"]


def fuel_cost(pos, crabs):
    return sum(int(abs(crab - pos)) for crab in crabs)


def part_1(input, verbose=False):
    crabs = list(sorted(parse_one_line_input(input)))

    median_crab_pos = median(crabs)
    if int(median_crab_pos) != median_crab_pos:
        print(f">>> median not an int: {median_crab_pos}")

    # median_up = ceil(median_crab_pos)
    # med_down = floor(median_crab_pos)

    return fuel_cost(median_crab_pos, crabs)


def part_2(input, verbose=False):
    pass


def day_7(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
