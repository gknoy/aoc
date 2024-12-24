"""
# https://adventofcode.com/2024/day/3
"""
import re

from aocd import get_data
from dataclasses import dataclass

input = get_data(day=3, year=2024).split("\n")

toy_input: list[str] = [
    # fmt: off
    "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    # fmt: on
]


# ============================
# part 1: parsing bullshit
# ============================
# instructions like "mul(X,Y)"
# no spaces / etc


# it's surely a trap to do this for part one but can fix later
MUL_X_MATCHER = re.compile(r"mul\(\d{1,3},\d{1,3}\)")
CMD_MATCHER = re.compile(r"(mul)\((\d{1,3}),(\d{1,3})\)")


def parse_line(line: str) -> list[str]:
    # e.g.  ['mul(2,4)', 'mul(5,5)', 'mul(11,8)', 'mul(8,5)']
    return MUL_X_MATCHER.findall(line)


class Operation:
    op = None

    def __init__(self, a, b):
        self.a = int(a)
        self.b = int(b)

    def value(self):
        raise NotImplementedError()


class Multiply(Operation):
    op = "mul"

    def value(self):
        return self.a * self.b


OPERATIONS = {
    "mul": Multiply,
}


def parse_command(cmd: str) -> Operation:
    # e.g.  "mul(2,4)" -> ('mul', '2', '4') -> Multiply(2, 4)
    op, a, b = CMD_MATCHER.match(cmd).groups()
    return OPERATIONS[op](a, b)


def part_1(input, verbose=False):
    line_ops = [
        # fmt: off
        [parse_command(cmd) for cmd in parse_line(line)]
        for line in input
        # fmt: on
    ]
    return sum(
        # fmt: off
        op.value()
        for line in line_ops
        for op in line
        # fmt: on
    )


def part_2(input, verbose=False):
    pass


def day_3(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
