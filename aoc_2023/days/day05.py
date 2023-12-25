"""
# https://adventofcode.com/2023/day/5
"""
from utils.utils import get_line_items

input = list(get_line_items("aoc_2023/input/05.txt"))
toy_input: list[str] = [
    # fmt: off
    "seeds: 79 14 55 13",
    "",
    "seed-to-soil map:",
    "50 98 2",
    "52 50 48",
    "",
    "soil-to-fertilizer map:",
    "0 15 37",
    "37 52 2",
    "39 0 15",
    "",
    "fertilizer-to-water map:",
    "49 53 8",
    "0 11 42",
    "42 0 7",
    "57 7 4",
    "",
    "water-to-light map:",
    "88 18 7",
    "18 25 70",
    "",
    "light-to-temperature map:",
    "45 77 23",
    "81 45 19",
    "68 64 13",
    "",
    "temperature-to-humidity map:",
    "0 69 1",
    "1 0 69",
    "",
    "humidity-to-location map:",
    "60 56 37",
    "56 93 4",
    # fmt: on
]


# ------------------
# Part 1
# ------------------
# Every type of seed, soil, fertilizer and so on is identified with a number
# Numbers are reused by each category
# soil 123 and fertilizer 123 aren't necessarily related\


def part_1(input, verbose=False):
    pass


# ------------------
# Part 2
# ------------------


def part_2(input, verbose=False):
    pass


def day_5(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
