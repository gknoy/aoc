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
MUL_MATCHER = re.compile(r"mul\(\d{1,3},\d{1,3}\)")
CMD_MATCHER = re.compile(r"(mul)\((\d{1,3}),(\d{1,3})\)")


def parse_line_part1(line: str) -> list[str]:
    # e.g.  ['mul(2,4)', 'mul(5,5)', 'mul(11,8)', 'mul(8,5)']
    return MUL_MATCHER.findall(line)


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


def parse_command_part1(cmd: str) -> Operation:
    # e.g.  "mul(2,4)" -> ('mul', '2', '4') -> Multiply(2, 4)
    op, a, b = CMD_MATCHER.match(cmd).groups()
    return OPERATIONS[op](a, b)


def part_1(input, verbose=False):
    line_ops = [
        # fmt: off
        [parse_command_part1(cmd) for cmd in parse_line_part1(line)]
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


# ============================
# part 2: More parsing bullshit
# ============================
# Can't iterate over them individually, need to track state of
# enable/disabled.
#
# Regexes were indeed a trap ;)
# DO_DONT_CMD_MATCHER = re.compile(
#     r"""
#     (do\(\))
#     |
#     (don't\(\))
#     |
#     ((mul)\((\d{1,3}),(\d{1,3})\))
#     """
# )


toy_input_two: list[str] = [
    # fmt: off
    "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    #                    ^^^^^^^                                ^^^^
    #                           |<-   Skipped               -->|
    # fmt: on
]

DO_MATCHER = re.compile(r"do\(\)")
DONT_MATCHER = re.compile(r"don't\(\)")
MULTIPLY_ARGS_MATCHER = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

ENABLE = "do()"
DISABLE = "don't()"
MUL_START = "mul("


def parse_tokens(line: str) -> list[str]:
    """Get the tokens that we see. DOES NOT CARE about enable/disable"""
    tokens = []
    line_len = len(line)
    pos = 0
    while pos < line_len:
        # I dislike the magic numbers for length of these strings,
        # but it's clear enough for now.
        if line[pos : pos + 4] == ENABLE:
            tokens.append(ENABLE)
            pos += 4
            continue
        elif line[pos : pos + 7] == DISABLE:
            tokens.append(DISABLE)
            pos += 7
            continue
        elif line[pos : pos + 4] == MUL_START:
            # we MIGHT be at the start of a multiplication.
            m = MULTIPLY_ARGS_MATCHER.match(line, pos)
            if m is None:
                pos += 1
            else:
                assert m.start() == pos
                pos = m.end()
                a, b = m.groups()
                tokens.append(Multiply(a, b))
        else:
            pos += 1
    return tokens


def part_2(input, verbose=False):
    """
    New instructions:
    - `do()`: enable 'mul'
    - `don't()`: disable 'mul'
    """
    enabled = True  # only most recent enable/disable is needed

    total = 0

    for line in input:
        # scan for tokens on the line
        tokens = parse_tokens(line)
        for token in tokens:
            if token == ENABLE:
                enabled = True
                continue
            if token == DISABLE:
                enabled = False
                continue
            if enabled:
                # token is a 'mul(a,b)' operation
                total += token.value()
    return total


def day_3(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    data2 = toy_input_two if use_toy_data else input
    return [part_1(data, verbose), part_2(data2, verbose)]
