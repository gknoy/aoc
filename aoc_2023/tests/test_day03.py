"""
# https://adventofcode.com/2023/day/3
"""
from aoc_2023.days.day03 import input, toy_input, part_1, parse_line, PartNumber, Symbol


def test_parse_line():
    line = ".13..+.58."
    #       0123456789
    expected = [
        PartNumber(value=13, start=1, end=3),
        Symbol(name="+", start=5, end=6),
        PartNumber(value=58, start=7, end=9),
    ]


# def test_part_1_toy():
#     assert part_1(toy_input) == 4361


# def test_part_1_real():
#     assert part_1(input) == "FIXME"


# def test_part_2_toy():
#     assert part_2(toy_input) == "FIXME"


# def test_part_2_real():
#     assert part_2(input) == "FIXME"
