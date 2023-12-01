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

FIRST_DIGIT_v1 = re.compile(r"\d")
LAST_DIGIT_v1 = re.compile(r".*(\d).*?")


def parse_calibration_v1(line: str) -> int:
    # get first and last digits
    first = FIRST_DIGIT_v1.search(line).group(0)
    # only one group
    # first group is whole string, second is what we want:
    last = LAST_DIGIT_v1.search(line).group(1)
    return int(f"{first}{last}")  # concat digits


def part_1(input, verbose=False):
    calibration_values = (parse_calibration_v1(line) for line in input)
    return sum(calibration_values)


# ==============================
# Part 2
# ==============================
#
# strings naming digits also count as digits

toy_input_2 = [
    "two1nine",  # 29
    "eightwothree",  # 83
    "abcone2threexyz",  # 13
    "xtwone3four",  # 24
    "4nineeightseven2",  # 42
    "zoneight234",  # 84
    "7pqrstsixteen",  # 76
]

FIRST_DIGIT_v2 = re.compile(r"(\d|one|two|three|four|five|six|seven|eight|nine|zero)")
LAST_DIGIT_v2 = re.compile(
    r".*(\d|one|two|three|four|five|six|seven|eight|nine|zero).*?"
)
DIGITS = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "0": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "zero": 0,
}


def parse_calibration_v2(line: str) -> int:
    """
    Concatenate first and last found digits, return int(digits)
    digit names ("one") count as a digit too
    """
    # There's a fancy find-all-matching-substrings algorithm
    # that someone mentioned on HN, but I didn't know about it before
    # doing this.  Might refactor later if performance bothers me ;)
    first = DIGITS[FIRST_DIGIT_v2.search(line).group(1)]
    last = DIGITS[LAST_DIGIT_v2.search(line).group(1)]
    return int(f"{first}{last}")  # concat digits


def part_2(input, verbose=False):
    calibration_values = (parse_calibration_v2(line) for line in input)
    return sum(calibration_values)


def day_1(use_toy_data=False, verbose=False):
    data1 = toy_input if use_toy_data else input
    data2 = toy_input_2 if use_toy_data else input
    return [part_1(data1, verbose), part_2(data2, verbose)]
