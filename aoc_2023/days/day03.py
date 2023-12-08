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
# Symbol: any character that isn't a digit and isn't a '.'
# Any number adjacent to a symbol, even diagonally, is a "part number"


@dataclass
class Item:
    start: int = 0
    end: int = 0


@dataclass
class Symbol(Item):
    name: str = None


@dataclass
class PartNumber(Item):
    value: int | str = None


@functools.cache
def is_digit(c: str) -> bool:
    return c in "0123456789"


@functools.cache
def is_symbol(c: str) -> bool:
    return c != "." and not is_digit(c)


def parse_line(line: str) -> list[Item]:
    digits = ""
    first = 0
    last = 0
    found = []

    def _save_part_number():
        if len(digits):
            value = int(digits)
            found.append(PartNumber(start=first, end=last, value=value))

    for index in range(len(line)):
        c = line[index]

        if is_digit(c):
            digits += c
            last = index
            # WTF... how did this even work right the first time?
        if c == ".":
            _save_part_number()
            digits = ""
            first = last = index
        if is_symbol(c):
            found.append(Symbol(name=c, start=first, end=last))
            first = last = index


def part_1(input, verbose=False):
    grid = [parse_line(line) for line in input]
    return "FIXME"


def part_2(input, verbose=False):
    pass


def day_3(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
