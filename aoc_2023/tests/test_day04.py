"""
# https://adventofcode.com/2023/day/4
"""
from aoc_2023.days.day04 import input, toy_input, part_1, part_2


def test_part_1_toy():
    assert part_1(toy_input) == 13


def test_part_1_real():
    assert part_1(input) == 24706


def test_part_2_toy():
    assert part_2(toy_input) == 30


def test_part_2_real():
    assert part_2(input) == 13114317
