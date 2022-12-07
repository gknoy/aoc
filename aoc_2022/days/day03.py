"""
# https://adventofcode.com/2022/day/3
"""
from functools import reduce
from itertools import islice
from typing import List, Tuple, Set
from utils.utils import get_line_items

input = list(get_line_items("aoc_2022/input/03.txt"))
toy_input: List[str] = [
    "vJrwpWtwJgWrhcsFMMfFFhFp",
    "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
    "PmmdzqPrVvPwwTWBwg",
    "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
    "ttgJtRGJQctTZtZT",
    "CrZsJsPPZsGzwwsLwLmpwMDw",
]

# ---------------------------------
# Part 1
# ---------------------------------


def get_rucksack(line: str) -> Tuple[Set, Set]:
    n_items = len(line)
    partition_index = int(n_items / 2)
    return (set(line[:partition_index]), set(line[partition_index:]))


def calc_priority(char: str) -> int:
    """
    a-z: 1-26
    A-Z: 27 - 52
    """
    # ord(A) == 65, ord(a) == 97"
    if char < "a":
        return ord(char) - 38  # ord("A") - 52
    return ord(char) - 96


def test_get_rucksack():
    line = "PmmdzqPrVvPwwTWBwg"
    assert get_rucksack(line) == (set("PmmdzqPrV"), set("vPwwTWBwg"))


def test_priority():
    assert calc_priority("a") == 1
    assert calc_priority("z") == 26
    assert calc_priority("A") == 27
    assert calc_priority("Z") == 52


def part_1(input, verbose=False):
    """
    For example, suppose you have the following list of contents from six rucksacks:

    vJrwpWtwJgWrhcsFMMfFFhFp
    jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    PmmdzqPrVvPwwTWBwg
    wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ttgJtRGJQctTZtZT
    CrZsJsPPZsGzwwsLwLmpwMDw

    The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp,
    which means its first compartment contains the items vJrwpWtwJgWr,
    while the second compartment contains the items hcsFMMfFFhFp.
    The only item type that appears in both compartments is lowercase p.

    The second rucksack's compartments contain jqHRNqRjqzjGDLGL and rsFMfFZSrLrFZsSL.
    The only item type that appears in both compartments is uppercase L.
    The third rucksack's compartments contain PmmdzqPrV and vPwwTWBwg; the only common item type is uppercase P.

    The fourth rucksack's compartments only share item type v.
    The fifth rucksack's compartments only share item type t.
    The sixth rucksack's compartments only share item type s.
    To help prioritize item rearrangement, every item type can be converted to a priority:

    Lowercase item types a through z have priorities 1 through 26.
    Uppercase item types A through Z have priorities 27 through 52.

    In the above example, the priority of the item type that appears in both compartments of each rucksack is
    16 (p), 38 (L), 42 (P), 22 (v), 20 (t), and 19 (s); the sum of these is 157.

    Find the item type that appears in both compartments of each rucksack.
    What is the sum of the priorities of those item types?
    """

    rucksacks = [get_rucksack(line) for line in input]

    # according to the prompt, this will be a set of likely 1 item
    common_items = [a & b for a, b in rucksacks]
    priority_sum = sum(
        [sum([calc_priority(item) for item in items]) for items in common_items]
    )
    return priority_sum


# ---------------------------------
# Part 2
# ---------------------------------


def group_elves(group_size: int, data: List) -> List[List]:
    data_iter = iter(data)
    groups = []
    group = list(islice(data_iter, group_size))
    while len(group):
        groups.append(group)
        group = list(islice(data_iter, group_size))
    return groups


def get_common_item(group: List[str]) -> str:
    # per problem set, this will be a set of only one overlap
    sets = map(set, group)
    item_set = reduce(lambda a, b: a & b, sets)
    return item_set.pop()


def part_2(input, verbose=False):
    """
    Every set of three lines in your list corresponds to a single group,
    but each group can have a different badge item type.
    So, in the above example, the first group's rucksacks are the first three lines:

        vJrwpWtwJgWrhcsFMMfFFhFp
        jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
        PmmdzqPrVvPwwTWBwg

    And the second group's rucksacks are the next three lines:

        wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
        ttgJtRGJQctTZtZT
        CrZsJsPPZsGzwwsLwLmpwMDw

    In the first group, the only item type that appears in all three rucksacks
    is lowercase r; this must be their badges.
    In the second group, their badge item type must be Z.

    Priorities for these items must still be found ...
    they are 18 (r) for the first group and 52 (Z) for the second group.
    The sum of these is 70.

    Find the item type that corresponds to the badges of each three-Elf group.
    What is the sum of the priorities of those item types?
    """
    groups = group_elves(3, input)
    return sum(map(calc_priority, map(get_common_item, groups)))


def day_3(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
