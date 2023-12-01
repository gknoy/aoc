"""
# https://adventofcode.com/2023/day/1
"""
from aoc_2023.days.day01 import input, toy_input, toy_input_2, part_1, part_2


def test_part_1_toy():
    assert part_1(toy_input) == 142


def test_part_1_real():
    assert part_1(input) == 56465


def test_part_2_toy():
    assert part_2(toy_input_2) == 281


def test_part_2_real():
    assert part_2(input) == 55902
