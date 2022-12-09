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


def test_get_boxes_and_instructions():
    boxes, instructions = get_boxes_and_instructions(toy_input)
    assert [boxes, instructions] == [
        ["    [D]", "[N] [C]", "[Z] [M] [P]", " 1   2   3"],
        [
            "move 1 from 2 to 1",
            "move 3 from 1 to 3",
            "move 2 from 2 to 1",
            "move 1 from 1 to 2",
        ],
    ]


class BadInputError(Exception):
    pass


def parse_move(instruction: str) -> MoveOrder:
    m = MOVE_PATTERN.match(instruction)
    if not m:
        raise BadInputError(instruction)
    n, s, d = map(int, m.groups())
    return MoveOrder(n, s, d)


def test_parse_move():
    assert parse_move("move 3 from 2 to 1") == MoveOrder(n_boxes=3, source=2, dest=1)


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


def test_get_stacks_of_boxes():
    boxes = ["    [D]", "[N] [C]", "[Z] [M] [P]", " 1   2   3"]
    assert get_stacks_of_boxes(boxes) == [
        # fmt: off
        ["Z", "N"],
        ["M", "C", "D"],
        ["P"],
        # fmt: on
    ]


EXPECTED_REAL_STACKS = [
    # fmt: off
    ["R", "N", "F", "V", "L", "J", "S", "M"],
    ["P", "N", "D", "Z", "F", "J", "W", "H"],
    ["W", "R", "C", "D", "G"],
    ["N", "B", "S"],
    ["M", "Z", "W", "P", "C", "B", "F", "N"],
    ["P", "R", "M", "W"],
    ["R", "T", "N", "G", "L", "S", "W"],
    ["Q", "T", "H", "F", "N", "B", "V"],
    ["L", "M", "H", "Z", "N", "F"],
    # fmt: on
]


def test_real_stacks():
    boxes = """
    [M] [H]         [N]
    [S] [W]         [F]     [W] [V]
    [J] [J]         [B]     [S] [B] [F]
    [L] [F] [G]     [C]     [L] [N] [N]
    [V] [Z] [D]     [P] [W] [G] [F] [Z]
    [F] [D] [C] [S] [W] [M] [N] [H] [H]
    [N] [N] [R] [B] [Z] [R] [T] [T] [M]
    [R] [P] [W] [N] [M] [P] [R] [Q] [L]
     1   2   3   4   5   6   7   8   9
    """.split(
        "\n"
    )
    assert get_stacks_of_boxes(boxes) == EXPECTED_REAL_STACKS


def test_move_one_at_a_time():
    stacks = [
        # fmt: off
        ["Z", "N"],
        ["M", "C", "D"],
        ["P"],
        # fmt: on
    ]
    move_one_box_at_a_time(stacks, MoveOrder(2, 2, 1))
    assert stacks == [
        # fmt: off
        ["Z", "N", "D", "C"],
        ["M"],
        ["P"],
        # fmt: on
    ]
    move_one_box_at_a_time(stacks, MoveOrder(1, 1, 3))
    assert stacks == [
        # fmt: off
        ["Z", "N", "D"],
        ["M"],
        ["P", "C"],
        # fmt: on
    ]


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
