"""
# https://adventofcode.com/2021/day/14
"""
from collections import Counter
from typing import Dict, List, Tuple
from utils import get_line_items

input = list(get_line_items("input/14.txt"))
toy_input: List[str] = [
    "NNCB",  # starting polymer
    "",
    "CH -> B",  # insertion rules
    "HH -> N",
    "CB -> H",
    "NH -> C",
    "HB -> C",
    "HC -> B",
    "HN -> C",
    "NN -> C",
    "BH -> H",
    "NC -> B",
    "NB -> B",
    "BN -> B",
    "BB -> N",
    "BC -> B",
    "CC -> N",
    "CN -> C",
]


def parse_rule(rule: str) -> Tuple[str, str]:
    """
    "CC -> N" => ("CC", "N")
    """
    pair, insertion = rule.split(" -> ")
    # replacement = f"{pair[0]}{insertion}{pair[1]}"
    return (pair, insertion)


def parse_input(lines) -> Tuple[str, Dict[str, str]]:
    polymer = lines[0]
    raw_rules = lines[2:]  # ["CH -> B", ...]
    rules = dict(parse_rule(rule) for rule in raw_rules)  # {"CH": "B", ...}
    return polymer, rules


def insert_items(polymer, rules, verbose=False):
    """
    Template:     NNCB
    Rules: {"NN": "C", "}
    After step 1: NCNBCHB
                   ^ ^ ^ inserted
    :param polymer:
    :param rules:
    :return:
    """
    chars = []
    if verbose:
        print(f">>> insert_items\n    polymer: {polymer}\n    rules: {rules}")
    for index in range(0, len(polymer) - 1):
        pair = polymer[index : index + 2]
        chars.append(polymer[index])
        if verbose:
            print(f"    ---- pair: {pair}  insertion: {rules[pair]}")
        if pair in rules:
            chars.append(rules[pair])
        # don't insert last of pair, as it's going to be first of the next pair
    # insert last one, since it's not the first of any pair
    chars.append(polymer[-1])
    return "".join(chars)


def part_1(input, verbose=False):
    """
    Apply 10 steps of pair insertion to the polymer template and
    find the most and least common elements in the result.
    What do you get if you take the quantity of the most common element and
    subtract the quantity of the least common element?
    """
    polymer, rules = parse_input(input)

    for iteration in range(0, 10):
        polymer = insert_items(polymer, rules, verbose=verbose)
        if verbose:
            print(f">>> {iteration:>3} {polymer}")

    counts = Counter([char for char in polymer])
    ordered_counts = counts.most_common()  # ordered high to low
    if verbose:
        print(f"    {counts}")
        print(f"    {ordered_counts}")

    most_common = ordered_counts[0][1]  # get the count part of the tuple
    least_common = ordered_counts[-1][1]
    if verbose:
        print(f">>> most common:  {most_common}")
        print(f">>> least common: {least_common}")
    return most_common - least_common


def part_2(input, verbose=False):
    pass


def day_14(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
