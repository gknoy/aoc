"""
# https://adventofcode.com/2022/day/4
"""
import pytest

from aoc_2022.days.day04 import input, toy_input, part_1, part_2, Range, parse_pair


def test_contains():
    assert Range(2, 9).contains(Range(3, 7))
    assert Range(2, 4).contains(Range(2, 4))


@pytest.mark.parametrize(
    "line,expected",
    [
        ["2-4,6-8", False],
        ["2-3,4-5", False],
        ["5-7,7-9", True],
        ["2-8,3-7", True],
        ["6-6,4-6", True],
        ["2-6,4-8", True],
    ],
)
def test_overlap(line, expected):
    a, b = parse_pair(line)
    assert a.overlaps(b) == expected
    assert b.overlaps(a) == expected


def test_parse_pair():
    assert parse_pair("2-4,6-8") == [Range(2, 4), Range(6, 8)]


def test_part_1_toy():
    assert part_1(toy_input) == 2


def test_part_1_real():
    assert part_1(input) == 556


def test_part_2_toy():
    assert part_2(toy_input) == 4


def test_part_2_real():
    assert part_2(input) == 876
