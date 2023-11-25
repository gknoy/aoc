"""
# https://adventofcode.com/2022/day/3
"""
from aoc_2022.days.day03 import (
    input,
    toy_input,
    part_1,
    part_2,
    get_rucksack,
    calc_priority,
)


def test_get_rucksack():
    line = "PmmdzqPrVvPwwTWBwg"
    assert get_rucksack(line) == (set("PmmdzqPrV"), set("vPwwTWBwg"))


def test_priority():
    assert calc_priority("a") == 1
    assert calc_priority("z") == 26
    assert calc_priority("A") == 27
    assert calc_priority("Z") == 52


def test_part_1_toy():
    assert part_1(toy_input) == 157


def test_part_1_real():
    assert part_1(input) == 7831


def test_part_2_toy():
    assert part_2(toy_input) == 70


def test_part_2_real():
    assert part_2(input) == 2683
