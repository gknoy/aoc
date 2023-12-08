"""
# https://adventofcode.com/2023/day/3
"""
import functools
from dataclasses import dataclass

from utils.utils import get_line_items

input = list(get_line_items("aoc_2023/input/03.txt"))
toy_input: list[str] = [
    # fmt: off
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
    # fmt: on
]

# -----------------------------
# Part 1
# -----------------------------
# Any number adjacent to a symbol, even diagonally, is a "part number"


@functools.cache
def is_digit(c: str) -> bool:
    return c in "0123456789"


@functools.cache
def is_symbol(c: str) -> bool:
    return c != "." and not is_digit(c)


@dataclass
class Item:
    value: int|str
    start: int = 0
    stop: int = 0


class Symbol(Item):
    pass



def parse_part_number(line, position):
    # return int() of all the digits that are connected to position in line
    return None


def part_1(input, verbose=False):
    grid = input
    pass


def part_2(input, verbose=False):
    pass


def day_3(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
