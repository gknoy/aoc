"""
# https://adventofcode.com/2024/day/1
"""
from aocd import get_data
from collections import Counter

# input = list(get_line_items("aoc_2024/input/01.txt"))
input = get_data(day=1, year=2024).split("\n")

toy_input: list[str] = [
    # fmt: off
    "3   4",
    "4   3",
    "2   5",
    "1   3",
    "3   9",
    "3   3",
    # fmt: on
]

# ====================================
# Part 1: Distances
# ====================================


def parse_lines_into_two_unsorted_lists(input: list[str]) -> tuple[list[int]]:
    """
    input: rows of strings representing pairs of nubmers
    This is almost certainly different from what we need in
    """
    a_items = []
    b_items = []

    for line in input:
        a, b = map(int, line.split())
        a_items.append(a)
        b_items.append(b)

    return (a_items, b_items)


def part_1(input, verbose=False):
    """
    # - sort the items in each column
    # - pair up each (e.g. (smallest from A, smallest from B))
    # - add up instances between items in each pair
    """
    a_items, b_items = map(sorted, parse_lines_into_two_unsorted_lists(input))

    pairs = [(a, b) for a, b in zip(a_items, b_items)]

    return sum(abs(a - b) for a, b in pairs)


# ====================================
# Part 2: Similarlty of left to right list
# ====================================


def part_2(input, verbose=False):
    """
    - Count how often each number from the left list appears in the right list.
    - similarity score: add each from left after multiplying by how often in the right.
    """
    a_items, b_items = parse_lines_into_two_unsorted_lists(input)
    b_counts = Counter(b_items)

    total_similarities = sum(
        item * b_counts[item] for item in a_items  # Counter gives zero for items it hasn't seen
    )
    return total_similarities


def day_1(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
