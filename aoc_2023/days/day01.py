"""
# https://adventofcode.com/2023/day/1
"""
import re

from utils.utils import get_line_items

input = list(get_line_items("aoc_2023/input/01.txt"))
toy_input: list[str] = [
    # fmt: off
    "1abc2",
    "pqr3stu8vwx",
    "a1b2c3d4e5f",
    "treb7uchet",
    # fmt: on
]

# ==============================
# Part 1
# ==============================
# On each line, the calibration value can be found by combining
# the first digit and the last digit (in that order)
# to form a single two-digit number.

# DIGITS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
FIRST_DIGIT = re.compile(r'\d')
LAST_DIGIT = re.compile(r'.*(\d).*?')


def parse_calibration_v1(line: str) -> int:
    # get first and last digits
    first = FIRST_DIGIT.search(line).group(0)
    # only one group
    # first group is whole string, second is what we want:
    last = LAST_DIGIT.search(line).group(1)
    return int(f"{first}{last}") # concat digits


def part_1(input, verbose=False):
    calibration_values = (
        parse_calibration_v1(line)
        for line in input
    )
    return sum(calibration_values)


def part_2(input, verbose=False):
    pass


def day_1(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
