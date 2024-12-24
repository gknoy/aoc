"""
# https://adventofcode.com/2024/day/3
"""
from aocd import get_data

input = get_data(day=3, year=2024).split("\n")

toy_input: list[str] = [
    # fmt: off
    "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    # fmt: on
]


def part_1(input, verbose=False):
    pass


def part_2(input, verbose=False):
    pass


def day_3(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
