"""
# https://adventofcode.com/2022/day/4
"""
from typing import List
from utils.utils import get_line_items

input = list(get_line_items("aoc_2022/input/04.txt"))
toy_input: List[str] = [
    # fmt: off
    "2-4,6-8",
    "2-3,4-5",
    "5-7,7-9",
    "2-8,3-7",
    "6-6,4-6",
    "2-6,4-8",
    # fmt: on
]


class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def contains(self, other):
        return self.start <= other.start and self.end >= other.end

    def overlaps(self, other):
        return (
            # case 1: we are leftward of other
            # ....567..  5-7
            # ......789  7-9
            (self.start <= other.start and self.end >= other.start)
            or
            # case 2: we are rightward of other
            # ......789  7-9
            # ....567..  5-7
            (self.start <= other.end and self.end >= other.start)
        )

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end


def parse_pair(line: str) -> List[Range]:
    tuples = line.split(",")
    return [Range(*map(int, item.split("-"))) for item in tuples]


def part_1(input, verbose=False):
    """
    Number pairs represent ranges. In how many pairs is one range included in the other one?
    """
    pairs = map(parse_pair, input)
    return sum([1 if a.contains(b) or b.contains(a) else 0 for a, b in pairs])


def part_2(input, verbose=False):
    pairs = map(parse_pair, input)
    return sum([1 if a.overlaps(b) else 0 for a, b in pairs])


def day_4(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
