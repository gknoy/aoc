"""
# https://adventofcode.com/2023/day/4
"""
from utils.utils import get_line_items

input = list(get_line_items("aoc_2023/input/04.txt"))
toy_input: list[str] = [
    # fmt: off
    #        (winning)      | (your card numbers)
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
    # fmt: on
]

# ---------------------
# Part 1: Scratchcards
# ---------------------
# first match makes the card worth one point
# each match after the first doubles the point value of that card


def part_1(input, verbose=False):
    pass


def part_2(input, verbose=False):
    pass


def day_4(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
