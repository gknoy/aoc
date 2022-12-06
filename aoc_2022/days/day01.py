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


def get_elf_calories(input):
    elves = []
    current = []
    for item in input:
        if item == "":
            elves.append(current)
            current = []
            continue
        current.append(int(item))
    # handle the last item if there is one ;)
    if len(current):
        elves.append(current)
    return elves


def part_1(input, verbose=False):
    """
    Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
    """
    elves = get_elf_calories(input)
    return max([sum(items) for items in elves])


def part_2(input, verbose=False):
    """
    Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?
    """
    elves = get_elf_calories(input)
    sorted_elves = list(sorted(elves, reverse=True, key=lambda elf_cals: sum(elf_cals)))
    return sum([sum(elf) for elf in sorted_elves[:3]])


def day_1(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
