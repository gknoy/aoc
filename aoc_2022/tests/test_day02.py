"""
# https://adventofcode.com/2022/day/2
"""
import pytest
from aoc_2022.days.day02 import input, toy_input, part_1, part_2, score, R, P, S


@pytest.mark.parametrize(
    "move,opponent,eq,win,lose,points",
    [
        # equal things
        [R, R, True, False, False, 3 + 1],
        [P, P, True, False, False, 3 + 2],
        [S, S, True, False, False, 3 + 3],
        # wins
        [R, S, False, True, False, 6 + 1],
        [P, R, False, True, False, 6 + 2],
        [S, P, False, True, False, 6 + 3],
        # losses
        [R, P, False, False, True, 0 + 1],
        [P, S, False, False, True, 0 + 2],
        [S, R, False, False, True, 0 + 3],
    ],
)
def test_score(move, opponent, eq, win, lose, points):
    assert eq == (move == opponent)
    assert lose == (move < opponent)
    assert win == (move > opponent)
    assert points == score(move, opponent)


def test_part_1_toy():
    assert part_1(toy_input) == 15


def test_part_1_real():
    assert part_1(input) == 10404


def test_part_2_toy():
    assert part_2(toy_input) == 12


def test_part_2_real():
    assert part_2(input) == 10334
