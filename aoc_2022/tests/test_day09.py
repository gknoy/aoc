"""
# https://adventofcode.com/2022/day/9
"""
import pytest
from aoc_2022.days.day09 import (
    Direction,
    Command,
    Position,
    Rope_v1,
    Rope_v2,
    input,
    toy_input,
    part_1,
    part_2,
    parse_input,
    to_steps,
)

# ----------------------
# Tests of Commands and Directions
# ----------------------


def test_command_equality():
    a = Command(Direction.UP, 3)
    b = Command(Direction.UP, 3)
    assert a == b


def test_command_to_steps():
    c = Command(direction=Direction.RIGHT, distance=4)
    assert c.to_steps() == [
        Command(direction=Direction.RIGHT, distance=1),
        Command(direction=Direction.RIGHT, distance=1),
        Command(direction=Direction.RIGHT, distance=1),
        Command(direction=Direction.RIGHT, distance=1),
    ]


def test_to_steps():
    commands = [Command(Direction.RIGHT, 3), Command(Direction.UP, 2)]
    expected = [
        Command(direction=Direction.RIGHT, distance=1),
        Command(direction=Direction.RIGHT, distance=1),
        Command(direction=Direction.RIGHT, distance=1),
        Command(direction=Direction.UP, distance=1),
        Command(direction=Direction.UP, distance=1),
    ]
    assert to_steps(commands) == expected


# ----------------------
# parsing tests
# ----------------------


def test_parse_input():
    assert parse_input(["R 4", "U 4", "L 3"]) == [
        Command(Direction.RIGHT, 4),
        Command(Direction.UP, 4),
        Command(Direction.LEFT, 3),
    ]


# ----------------------
# position tests
# ----------------------


@pytest.mark.parametrize(
    "a, b, expected",
    [
        # same-axis movement only
        [Position(0, 0), Position(2, 0), 2],
        # only diagonal
        [Position(0, 0), Position(2, 2), 2],
        [Position(0, 0), Position(-2, -2), 2],
        # examples from rope_distance docstring
        [Position(0, 0), Position(3, 1), 3],  # 1 diagonal
        [Position(0, 0), Position(3, 4), 4],  # 4 diagonals
    ],
)
def test_rope_distance(a, b, expected):
    assert a.rope_distance(b) == expected
    assert b.rope_distance(a) == expected


# ----------------------
# Rope calculation tests
# ----------------------


@pytest.mark.parametrize(
    "a, b, adjacent",
    [
        [Position(2, 2), Position(2, 2), True],
        # adjacent spaces
        [Position(2, 2), Position(2, 1), True],
        [Position(2, 2), Position(2, 3), True],
        [Position(2, 2), Position(1, 2), True],
        [Position(2, 2), Position(3, 2), True],
        # diagonals
        [Position(2, 2), Position(3, 3), True],
        [Position(2, 2), Position(1, 3), True],
        [Position(2, 2), Position(3, 1), True],
        [Position(2, 2), Position(1, 1), True],
        # NOT adjacent
        [Position(2, 2), Position(4, 4), False],
        [Position(2, 2), Position(2, 4), False],
        [Position(2, 2), Position(4, 2), False],
    ],
)
def test_pos_is_adjacent(a, b, adjacent):
    assert a.is_adjacent(b) == adjacent
    assert b.is_adjacent(a) == adjacent


@pytest.mark.parametrize(
    "a, b, closest",
    [
        # overlap
        [Position(0, 0), Position(0, 0), Position(0, 0)],
        # adjacent
        [Position(0, 0), Position(1, 1), Position(0, 0)],
        # head has moved out of range
        [Position(0, 0), Position(2, 1), Position(1, 1)],
        # diagonal movement
        [Position(0, 0), Position(2, 2), Position(1, 1)],
    ],
)
def test_closest_adjacent_position(a, b, closest):
    rope = Rope_v1(a, b)
    assert rope.closest_adjacent_pos(a, b) == closest
    # this isn't reflexive, as this models behavior of tail (a) of the rope


@pytest.mark.parametrize(
    "name, start_coords, direction, expected_coords",
    [
        # fmt:off
        # Adjacency positions: (tail assumed to be at E)
        #   A B C
        #   D E F
        #   G H I
        # (All coords are in (head,tail) order)
        # Case A: head above-left tail
        ["A", [(-1, 1), (0, 0)], Direction.UP,    [(-1, 2), (-1, 1)]],
        ["A", [(-1, 1), (0, 0)], Direction.DOWN,  [(-1, 0), (0, 0)]],
        ["A", [(-1, 1), (0, 0)], Direction.LEFT,  [(-2, 1), (-1, 1)]],
        ["A", [(-1, 1), (0, 0)], Direction.RIGHT, [(0, 1), (0, 0)]],
        # Case B: head above tail
        # Case C: head above-right tail
        ["C", [(1, 1), (0, 0)], Direction.UP,    [(1, 2), (1, 1)]],
        ["C", [(1, 1), (0, 0)], Direction.DOWN,  [(1, 0), (0, 0)]],
        ["C", [(1, 1), (0, 0)], Direction.LEFT,  [(0, 1), (0, 0)]],
        ["C", [(1, 1), (0, 0)], Direction.RIGHT, [(2, 1), (1, 1)]],
        # Case D: head left of tail
        # Case E: head overlaps tail
        ["E", [(0, 0), (0, 0)], Direction.UP,    [(0, 1),  (0, 0)]],
        ["E", [(0, 0), (0, 0)], Direction.DOWN,  [(0, -1), (0, 0)]],
        ["E", [(0, 0), (0, 0)], Direction.LEFT,  [(-1, 0), (0, 0)]],
        ["E", [(0, 0), (0, 0)], Direction.RIGHT, [(1, 0),  (0, 0)]],
        # Case F: head right of tail
        ["F", [(1, 0), (0, 0)], Direction.UP,    [(1, 1), (0, 0)]],
        ["F", [(1, 0), (0, 0)], Direction.DOWN,  [(1, -1), (0, 0)]],
        ["F", [(1, 0), (0, 0)], Direction.LEFT,  [(0, 0), (0, 0)]],
        ["F", [(1, 0), (0, 0)], Direction.RIGHT, [(2, 0), (1, 0)]],
        # Case G: head bottom-left of tail
        # Case H: head below tail
        # Case I: head
        # fmt:on
    ],
)
def test_rope_v1_move_head(name, start_coords, direction, expected_coords):
    # name unused except for differentiating pytest runs ;)
    head, tail = [Position(*coords) for coords in start_coords]
    exp_head, exp_tail = [Position(*coords) for coords in expected_coords]
    rope = Rope_v1(head, tail)
    assert rope.head == head
    assert rope.tail == tail
    step = Command(direction=direction, distance=1)
    rope.move_head(step)
    assert rope.head == exp_head, "unexpected head location"
    assert rope.tail == exp_tail, "unexpected tail location"


# ----------------------
# Final tests
# ----------------------


def test_part_1_toy():
    result = part_1(toy_input)
    assert part_1(toy_input) == 13


def test_part_2_toy():
    assert part_2(toy_input) == 1


def test_part2_toy2():
    toy2 = [
        "R 5",
        "U 8",
        "L 8",
        "D 3",
        "R 17",
        "D 10",
        "L 25",
        "U 20",
    ]
    assert part_2(toy2) == 36


def test_part_1_real():
    assert part_1(input) == 6486


def test_part_2_real():
    assert part_2(input) == 2678
