"""
# https://adventofcode.com/2021/day/6
"""
from collections import defaultdict

from utils.utils import get_line_items, parse_one_line_input

input = list(get_line_items("aoc_2021/input/06.txt"))
toy_input = ["3,4,3,1,2"]


def init_fish_buckets(input, max_cd=8):
    """
    Make a list of fish-counts, bucketed by their spawn cooldown,

    [3, 4, 3, 1, 2] -> [0, 1, 1, 2, 1, 0, 0, 0, 0]
    """
    buckets = defaultdict(int)
    for fish in input:
        buckets[fish] += 1

    return [buckets[cd] for cd in range(0, max_cd + 1)]


def day_iteration(
    cd_buckets, days_remaining=80, spawn_cd=6, newspawn_cd=8, verbose=False
):
    """
    Spawn day0 things, and move the rest left one CD

    cd:  |  0  1  2  3  4  5  6  7  8
    ---------------------------------
    in:  | [6, 1, 1, 2, 1, 0, 0, 0, 0]
    out: | [1, 1, 2, 1, 0, 0, 0+6, 0, 6]

    """
    if verbose:
        print(f"{days_remaining}: {cd_buckets}")
    if days_remaining == 0:
        return cd_buckets
    # moms have one baby eachs
    baby_fish = moms = cd_buckets[0]
    new_fish = cd_buckets[1:] + [0]  # always add a new day at max cd
    new_fish[spawn_cd] += moms
    new_fish[newspawn_cd] += baby_fish
    return day_iteration(new_fish, days_remaining - 1, spawn_cd, newspawn_cd, verbose)


def part_1(input, verbose=False):
    buckets = init_fish_buckets(input, max_cd=8)
    final_fish = day_iteration(buckets, days_remaining=80, verbose=verbose)
    return sum(final_fish)


def part_2(input, verbose=False):
    buckets = init_fish_buckets(input, max_cd=8)
    final_fish = day_iteration(buckets, days_remaining=256, verbose=verbose)
    return sum(final_fish)


def day_6(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    data = parse_one_line_input(data)
    return [part_1(data, verbose), part_2(data, verbose)]
