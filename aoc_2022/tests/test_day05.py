"""
# https://adventofcode.com/2022/day/5
"""
from aoc_2022.days.day05 import (
    input,
    toy_input,
    part_1,
    part_2,
    get_stacks_of_boxes,
    move_one_box_at_a_time,
    MoveOrder,
    parse_move,
    get_boxes_and_instructions,
)


def test_parse_move():
    assert parse_move("move 3 from 2 to 1") == MoveOrder(n_boxes=3, source=2, dest=1)


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


def test_part_1_toy():
    assert part_1(toy_input) == "CMZ"


def test_part_1_real():
    assert part_1(input) == "QPJPLMNNR"


def test_part_2_toy():
    assert part_2(toy_input) == "MCD"


def test_part_2_real():
    assert part_2(input) == "BQDNWJPVJ"
