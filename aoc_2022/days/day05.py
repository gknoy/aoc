"""
# https://adventofcode.com/2022/day/5
"""
from typing import List
from utils.utils import get_line_items

input = list(get_line_items("aoc_2022/input/05.txt"))
toy_input: List[str] = [
    # fmt: off
    "    [D]",
    "[N] [C]",
    "[Z] [M] [P]",
    " 1   2   3",
    "",
    "move 1 from 2 to 1",
    "move 3 from 1 to 3",
    "move 2 from 2 to 1",
    "move 1 from 1 to 2",
    # fmt: on
]

# ------------------------------
# Part 1:
# - crates moved one at a time
# - report top item on each stack
# ------------------------------


def part_1(input, verbose=False):
    """
    Crates are moved one at a time

                [Z]
                [N]
                [D]
        [C] [M] [P]
         1   2   3

    The Elves just need to know which crate will end up on top of each stack;
    in this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3,
    so you should combine these together and give the Elves the message CMZ.
    """
    pass


# ------------------------------
# Part 2
# ------------------------------


def part_2(input, verbose=False):
    pass


def day_5(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
