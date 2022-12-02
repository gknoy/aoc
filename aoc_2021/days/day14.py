"""
# https://adventofcode.com/2021/day/14
"""
import pytest
from collections import Counter, defaultdict
from math import ceil
from typing import Dict, List, Tuple
from utils.utils import get_line_items

input = list(get_line_items("aoc_2021/input/14.txt"))
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


# --------------------------------------
# Part 1: Simple approach is enough for 10 iterations
#   - store items in strings
#   - build strings with join or concatenate
#
#   This ends up NOT scaling when we try to go to 40 iterations, though.
# --------------------------------------


def insert_items_slow(polymer, rules, verbose=False):
    """
    Template:     NNCB
    Rules: {"NN": "C", "}
    After step 1: NCNBCHB
                   ^ ^ ^ inserted
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


def part_1(input, verbose=False, n_iterations=10):
    """
    Apply 10 steps of pair insertion to the polymer template and
    find the most and least common elements in the result.
    What do you get if you take the quantity of the most common element and
    subtract the quantity of the least common element?
    """
    polymer, rules = parse_input(input)

    for iteration in range(0, n_iterations):
        polymer = insert_items_slow(polymer, rules, verbose=verbose)
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


# ----------------------------------------------------
# Part 2: Failed attempt at faster (using linked list)
# ----------------------------------------------------
#
#     $ ./advent.py 14 --toy
#     # ... len of strings / iteration counts per step:
#     >>>  23 50331649
#
# My first thought is to model the polymer as a linked list, and do
# linked list insertions, so that I don't have to spend time re-allocating or
# re-concatenating things.
# Then, when looking at the final polymer, we can just count the items....
#
# Verdict: This is still super slow, because it's still iterating over
# the string, which rapidly gets way too large.
#
# ----------------------------------------------------
#
# class NodeIterator:
#     # TIL not to make the iterator the same as the node class ;)
#     def __init__(self, node):
#         self.node = node
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         if self.node is None:
#             raise StopIteration
#         current = self.node
#         self.node = self.node.next
#         return current
#
#
# class Node:
#     def __init__(self, char, node=None):
#         self.char = char
#         self.next = node
#         self.length = 1
#         if node is not None:
#             self.length += node.length
#
#     def __iter__(self):
#         return NodeIterator(self)
#
#     def __repr__(self):
#         return f"Node {self.char} -> {repr(self.next)}"
#
#     def insert(self, nodes: "Node"):
#         """Insert the sequence between me and my next pointer"""
#         if nodes is None:
#             return
#         last_item = nodes
#         while last_item.next is not None:
#             last_item = last_item.next
#         last_item.next = self.next
#         self.next = nodes
#         self.length += nodes.length
#
#     def get_pair(self):
#         if self.next is None:
#             return None
#         return self.char + self.next.char
#
#     def get_sequence(self) -> List[str]:
#         """test helper :)"""
#         return [item.char for item in self]
#
#
# def get_polymer_nodes(sequence: str) -> Node:
#     """
#     "ABC" -> Node("A", Node("B", Node("C", None)))
#     """
#     polymer = None
#     for char in reversed(sequence):
#         polymer = Node(char, polymer)
#     return polymer
#
#
# @pytest.mark.parametrize(
#     "seq,insert,expected",
#     [
#         ("NNCB", "XY", "NXYNCB"),
#         ("N", "X", "NX"),
#         ("N", Node("X", Node("Y")), "NXY"),
#         ("NNCB", None, "NNCB"),
#     ],
# )
# def test_node_methods(seq, insert, expected):
#     nodes = get_polymer_nodes(seq)
#     assert nodes.get_sequence() == list(seq)
#     to_insert = insert
#     if type(insert) is str:
#         to_insert = get_polymer_nodes(insert)  # "AB" -> nodes
#     nodes.insert(to_insert)
#     assert nodes.get_sequence() == list(expected)
#
#
# def insert_nodes_from_rules(polymer: Node, rules: Dict, verbose=False):
#     """
#     Polymer:     NNCB -- Node("N", Node("N", Node("C", Node("B", None))))
#     Rules: {"NN": "C", }
#     After step 1: NCNCB -- Node("N", Node("C", Node("N", Node("C", Node("B", None)))))
#                    ^ inserted        ^^^^^^^
#     """
#     # if verbose:
#     #     print(
#     #         f">>> insert_items\n    polymer: {str(polymer.get_sequence())}\n    rules: {rules}"
#     #     )
#
#     # we don't want to use `for node in polymer`, as that would also
#     # iterate over any inserted items.
#     node = polymer
#     while node is not None:
#         pair = node.get_pair()
#         # if verbose:
#         #     print(f" -- pair: {pair}")
#         # hold our next pointer so that we don't try to also
#         # iterate over the things we're inserting
#         next_node = node.next
#         if pair in rules:
#             node.insert(Node(rules[pair]))
#         node = next_node
#
#
# def test_rule_insertion():
#     seq = "NNCB"
#     nodes = get_polymer_nodes(seq)
#
#     rules = {"NN": "C", "NC": "B", "CB": "H"}
#     insert_nodes_from_rules(nodes, rules)
#     assert nodes.get_sequence() == list("NCNBCHB")
#
#
# def part_2(input, verbose=False, n_iterations=40):
#     """
#     Same as above, but with 40 iterations.
#     Each iteration ends up roughly doubling, so we end up with exponentially
#     longer time per iteration if we do it the naiive way:
#
#
#     This is FAR too many iterations to be efficient as the string gets longer,
#     especially since we're re-building the string + insertions
#     """
#     polymer_chars, rules = parse_input(input)
#     polymer = get_polymer_nodes(polymer_chars)
#
#     for iteration in range(0, n_iterations):
#         insert_nodes_from_rules(polymer, rules, verbose=verbose)
#         # if verbose:
#         print(f">>> {iteration:>3} {len(polymer.get_sequence())}")
#
#     counts = Counter([node.char for node in polymer])
#     ordered_counts = counts.most_common()  # ordered high to low
#     if verbose:
#         print(f"    {counts}")
#         print(f"    {ordered_counts}")
#
#     most_common = ordered_counts[0][1]  # get the count part of the tuple
#     least_common = ordered_counts[-1][1]
#     if verbose:
#         print(f">>> most common:  {most_common}")
#         print(f">>> least common: {least_common}")
#     return most_common - least_common


# ----------------------------------------------------
# Part 2: Keep a count of each tuple, but don't iterate the whole string.
# ----------------------------------------------------
#
# e.g.:
#   sequence = "NNCB" -> {NN: 1, NC: 1, CB: 1}
#   rules = {"NN": "C", "NC": "B", "CB": "H"}
#
#   { NN: 1,  ->  { NN: 0, NC: 1, CN: 1 } +    { NC; 1, CN: 1,
#     NC: 1,  ->  { NC: 0, NB: 1, BC: 1 } + =>   NB: 1, BC: 1,
#     CB: 1 } ->  { CB: 0, CH: 1, HB: 1 }        CH: 1, HB: 1 }
#
#   expected:
#   "NCNBCHB" -> { NC: 1, CN: 1, NB: 1, BC: 1, CH: 1, HB: 1 }
#
# When replacing in the next iteration, we DON'T CARE about the order of
# any of these pairs, just the counts for each tuple. In later iterations,
# when we
# ----------------------------------------------------


def get_pairs(seq):
    return [seq[index] + seq[index + 1] for index in range(0, len(seq) - 1)]


def get_pair_counts(pairs) -> Dict[str, int]:
    counts = defaultdict(int)
    counts.update(Counter(pairs))
    return counts


def get_polymer(seq):
    """Represent a polymer as counts-of-pairs"""
    return get_pair_counts(get_pairs(seq))


def normalize_counts(polymer):
    return {pair: count for pair, count in polymer.items() if count > 0}


def insert_replacements(polymer: Dict[str, int], rules: Dict[str, str]):
    count_deltas = defaultdict(int)
    for pair, count in polymer.items():
        insertion = rules.get(pair)
        if insertion is not None:
            left = pair[0] + insertion
            right = insertion + pair[1]
            count_deltas[pair] -= count
            count_deltas[left] += count
            count_deltas[right] += count
    for pair, count in count_deltas.items():
        polymer[pair] += count


@pytest.fixture
def toy_rules():
    # rules as parsed from toy data
    return {
        # fmt: off
        "BB": "N", "BC": "B", "BH": "H", "BN": "B", "CB": "H",
        "CC": "N", "CH": "B", "CN": "C", "HB": "C", "HC": "B",
        "HH": "N", "HN": "C", "NB": "B", "NC": "B", "NH": "C",
        "NN": "C",
        # fmt: on
    }


@pytest.mark.parametrize(
    "polymer,expected",
    [
        [get_polymer("NNCB"), get_polymer("NCNBCHB")],
        [get_polymer("NCNBCHB"), get_polymer("NBCCNBBBCBHCB")],
        [get_polymer("NBCCNBBBCBHCB"), get_polymer("NBBBCNCCNBBNBNBBCHBHHBCHB")],
        [
            get_polymer("NBBBCNCCNBBNBNBBCHBHHBCHB"),
            get_polymer("NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"),
        ],
    ],
)
def test_insert_replacements(polymer, expected, toy_rules):
    insert_replacements(polymer, toy_rules)
    assert (
        normalize_counts(polymer) == expected
    )  # default dict vs regular dict is still OK


def count_chars(polymer):
    char_counts = defaultdict(int)
    for pair, count in polymer.items():
        left, right = list(pair)
        char_counts[left] += count
        char_counts[right] += count
    # Sometimes there are odds here. I'm not sure why this works. ;)
    return Counter({char: ceil(count / 2) for char, count in char_counts.items()})


def test_count_chars():
    polymer = {
        # fmt: off
        "NC": 42, "CB": 115, "CN": 102, "NB": 796, "BC": 120, "CH": 21,
        "HB": 26, "CC": 60, "BB": 812, "BH": 81, "HC": 76,
        "BN": 735, "HH": 32, "HN": 27, "NH": 27,
        # fmt: on
    }
    assert count_chars(polymer) == {"N": 865, "C": 298, "B": 1749, "H": 161}


def part_2(input, verbose=False, n_iterations=40):
    """
    Same as above, but with 40 iterations.
    Each iteration ends up roughly doubling, so we end up with exponentially
    longer time per iteration if we do it the naive way.
    Instead of iterating along a representation of the polymer each time,
    we store counts for things we're doing replacemnts on.
    """
    polymer_chars, rules = parse_input(input)

    # this is just a dict of tuple counts:
    polymer = get_pair_counts(get_pairs(polymer_chars))

    for iteration in range(0, n_iterations):
        insert_replacements(polymer, rules)
        if verbose:
            print(f">>> {iteration:>3} {normalize_counts(polymer)}")

    counts = count_chars(polymer)
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


@pytest.mark.parametrize("n_iterations", list(range(1, 19)))
def test_same_answers(n_iterations):
    data = toy_input
    assert part_1(data, False, n_iterations) == part_2(data, False, n_iterations)


def day_14(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
