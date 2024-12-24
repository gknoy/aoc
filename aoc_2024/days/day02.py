"""
# https://adventofcode.com/2024/day/2
"""
from collections import Counter
from typing import Generator
from aocd import get_data

# input = list(get_line_items("aoc_2024/input/02.txt"))
input = get_data(day=2, year=2024).split("\n")

toy_input: list[str] = [
    # fmt: off
    "7 6 4 2 1",  # note length of report can differ
    "1 2 7 8 9",
    "9 7 6 2 1",
    "1 3 2 4 5",
    "8 6 4 4 1",
    "1 3 6 7 9",
    # fmt: on
]

# ==========================
# Part 1: safe/unsafe intervals
# ==========================


def parse_reports(input: list[str]) -> list[list[int]]:
    return [[int(item) for item in line.split()] for line in input]


def sign(n: int) -> int:
    if n == 0:
        return 0
    if n > 0:
        return 1
    return -1


def get_intervals(report: list[int]) -> list[int]:
    return [
        report[index + 1] - report[index]
        for index in range(0, len(report) - 1)
    ]


def is_safe(report, min_step=1, max_step=3, verbose=False):
    direction = None
    intervals = get_intervals(report)
    if verbose:
        print(f">>> is_safe: {intervals}")
    for step in intervals:
        print(f"   - step: {step}  dir: {sign(step)}")
        step_size = abs(step)
        if step_size < min_step or step_size > max_step:
            if verbose:
                print(f"  - False: {step_size < min_step} or {step_size > max_step}")
            return False
        # since min step is 1, for now
        # direction won't ever be zero
        if direction is None:
            direction = sign(step)
        if sign(step) != direction:
            if verbose:
                print(f"   - False: expected dir: {direction}")
            return False
    # Safe if we haven't failed yet (empty reports are also safe)
    return True


def part_1(input, verbose=False):
    """
    - Each report is a list of numbers called levels that are separated by spaces.
    - safe if both:
        - The levels are either all increasing or all decreasing.
        - Any two adjacent levels differ by at least one and at most three.
    """
    reports = parse_reports(input)
    safe_counter = Counter([
        is_safe(report, verbose=verbose)
        for report in reports
    ])
    return safe_counter[True]


def part_2(input, verbose=False):
    pass


def day_2(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
