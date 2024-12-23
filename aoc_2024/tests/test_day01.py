"""
# https://adventofcode.com/2024/day/1
"""
from aoc_2024.days.day01 import input, toy_input, part_1, part_2


def test_part_1_toy():
    assert part_1(toy_input) == 11


def test_part_1_real():
    assert part_1(input) == 1223326


def test_part_2_toy():
    assert part_2(toy_input) == 31


def test_part_2_real():
    assert part_2(input) == 21070419
