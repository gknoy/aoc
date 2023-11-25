"""
# https://adventofcode.com/2022/day/5
"""
import itertools
import re
from collections import defaultdict
from typing import List
from utils.utils import get_line_items

input = list(get_line_items("aoc_2022/input/05.txt"))
toy_input: List[str] = [
    # fmt: off
    "    [D]",
    "[N] [C]",
    "[Z] [M] [P]",
    " 1   2   3",
    "",
    "move 1 from 2 to 1",  # note that these are 1-indexed source/dest
    "move 3 from 1 to 3",
    "move 2 from 2 to 1",
    "move 1 from 1 to 2",
    # fmt: on
]

# ------------------------------
# Part 1:
# - crates moved one at a time
# - report top item on each stack
# ------------------------------

StackedBoxesType = List[List[str]]

MOVE_PATTERN = re.compile(r"move (\d+) from (\d+) to (\d+)")


class MoveOrder:
    def __init__(self, n_boxes: int, source: int, dest: int):
        self.n_boxes = n_boxes
        self.source = source - 1
        self.dest = dest - 1

    def __eq__(self, other):
        return (self.n_boxes, self.source, self.dest) == (
            other.n_boxes,
            other.source,
            other.dest,
        )

    def __repr__(self):
        return f"<MoveOrder {self.n_boxes} {self.source} {self.dest}>"


def get_boxes_and_instructions(input: List[str]) -> List[List[str]]:
    n_box_lines = len(list(itertools.takewhile(lambda line: len(line), input)))
    return [input[:n_box_lines], input[n_box_lines + 1 :]]


class BadInputError(Exception):
    pass


def parse_move(instruction: str) -> MoveOrder:
    m = MOVE_PATTERN.match(instruction)
    if not m:
        raise BadInputError(instruction)
    n, s, d = map(int, m.groups())
    return MoveOrder(n, s, d)


def get_stacks_of_boxes(box_ascii_art: List[str]) -> StackedBoxesType:
    # builds stacks in reverse, top-down, then reverse them
    stacks_by_raw_col = defaultdict(list)
    for row in box_ascii_art:
        for col, char in enumerate(row):
            if char not in "[ ]":
                stacks_by_raw_col[col].append(char)

    # go through each raw column's data, and make the proper stacks:
    return [
        list(reversed(stacks_by_raw_col[key][:-1]))
        for key in sorted(stacks_by_raw_col.keys())
    ]


def move_one_box_at_a_time(stacks: StackedBoxesType, move_order: MoveOrder) -> None:
    """
    Manipulate boxes (in place)
    """
    for iteration in range(move_order.n_boxes):
        stacks[move_order.dest].append(stacks[move_order.source].pop())


def part_1(input, verbose=False):
    """
    Crates are moved one at a time

                [Z]
                [N]
                [D]
        [C] [M] [P]
         1   2   3

    The Elves just need to know which crate will end up on top of each stack;
    in this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3,
    so you should combine these together and give the Elves the message CMZ.
    """
    boxes, raw_instructions = get_boxes_and_instructions(input)
    stacks = get_stacks_of_boxes(boxes)
    orders = [parse_move(instruction) for instruction in raw_instructions]

    for order in orders:
        move_one_box_at_a_time(stacks, order)

    last_in_each_stack = [stack[-1] for stack in stacks]
    return "".join(last_in_each_stack)


# ------------------------------
# Part 2
# ------------------------------


def move_n_boxes_at_a_time(stacks, move_order):
    n_boxes = move_order.n_boxes

    source_end = -1 * n_boxes
    top_boxes = stacks[move_order.source][source_end:]
    stacks[move_order.dest].extend(top_boxes)
    stacks[move_order.source] = stacks[move_order.source][:source_end]


def part_2(input, verbose=False):
    boxes, raw_instructions = get_boxes_and_instructions(input)
    stacks = get_stacks_of_boxes(boxes)
    orders = [parse_move(instruction) for instruction in raw_instructions]

    for order in orders:
        move_n_boxes_at_a_time(stacks, order)

    last_in_each_stack = [stack[-1] for stack in stacks if len(stack)]
    return "".join(last_in_each_stack)


def day_5(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
