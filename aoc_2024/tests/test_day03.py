"""
# https://adventofcode.com/2024/day/3
"""
from aoc_2024.days.day03 import input, toy_input, toy_input_two, part_1, part_2


def test_part_1_toy():
    assert part_1(toy_input) == 161


def test_part_1_real():
    assert part_1(input) == 187825547


def test_part_2_toy():
    assert part_2(toy_input_two) == 48


def test_part_2_real():
    result = part_2(input)
    assert result == 85508223, result
