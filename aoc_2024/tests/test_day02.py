"""
# https://adventofcode.com/2024/day/2
"""
from aoc_2024.days.day02 import input, toy_input, part_1, part_2


def test_part_1_toy():
    assert part_1(toy_input) == 2


def test_part_1_real():
    assert part_1(input) == 321


def test_part_2_toy():
    assert part_2(toy_input) == 4


def test_part_2_real():
    assert part_2(input) == 386
