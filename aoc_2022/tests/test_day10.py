"""
# https://adventofcode.com/2022/day/10
"""
from aoc_2022.days.day10 import input, toy_input, part_1, part_2


def test_part_1_toy():
    """
    During the 20th cycle, register X has the value 21, so the signal strength is 20 * 21 = 420. (The 20th cycle occurs in the middle of the second addx -1, so the value of register X is the starting value, 1, plus all of the other addx values up to that point: 1 + 15 - 11 + 6 - 3 + 5 - 1 - 8 + 13 + 4 = 21.)
    During the 60th cycle, register X has the value 19, so the signal strength is 60 * 19 = 1140.
    During the 100th cycle, register X has the value 18, so the signal strength is 100 * 18 = 1800.
    During the 140th cycle, register X has the value 21, so the signal strength is 140 * 21 = 2940.
    During the 180th cycle, register X has the value 16, so the signal strength is 180 * 16 = 2880.
    During the 220th cycle, register X has the value 18, so the signal strength is 220 * 18 = 3960.
    """
    assert part_1(toy_input) == 13140


def test_part_1_real():
    assert part_1(input) == 14520


# def test_part_2_toy():
#     assert part_2(toy_input) is not None  # FIXME: use actual expected values


# def test_part_2_real():
#     raise NotImplementedError
#     # result = part_2(input)
