"""
# https://adventofcode.com/2022/day/9
#
# rope movement
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional
import functools
import pytest

from utils.utils import get_line_items

input = list(get_line_items("aoc_2022/input/09.txt"))
toy_input: list[str] = [
    # fmt: off
    "R 4",
    "U 4",
    "L 3",
    "D 1",
    "R 4",
    "D 1",
    "L 5",
    "R 2",
    # fmt: on
]

# -----------------------------------------
# Part 1
# -----------------------------------------
#
# If the head is ever two steps directly up, down, left, or right from the tail,
# the tail must also move one step in that direction so it remains close enough:
#
# .....    .....    .....
# .TH.. -> .T.H. -> ..TH.
# .....    .....    .....
#
# ...    ...    ...
# .T.    .T.    ...
# .H. -> ... -> .T.
# ...    .H.    .H.
# ...    ...    ...
#
# Otherwise, if the head and tail aren't touching and aren't in the same row or column, the tail always moves one step diagonally to keep up:
#
# .....    .....    .....
# .....    ..H..    ..H..
# ..H.. -> ..... -> ..T..
# .T...    .T...    .....
# .....    .....    .....
#
# .....    .....    .....
# .....    .....    .....
# ..H.. -> ...H. -> ..TH.
# .T...    .T...    .....
# .....    .....    .....


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    RIGHT = "RIGHT"
    LEFT = "LEFT"

    @classmethod
    @functools.cache
    def parse(cls, s: str) -> "Direction":
        match s:
            case "U":
                return cls.UP
            case "D":
                return cls.DOWN
            case "R":
                return cls.RIGHT
            case "L":
                return cls.LEFT
        raise IndexError


@dataclass
class Command:
    direction: Direction
    distance: int

    def __str__(self):
        return f"({self.direction} {self.distance})"

    def to_steps(self) -> list["Command"]:
        """
        Get a list of commands with distance 1
        e.g.  (R 4) -> [(R 1), (R 1), (R 1), (R 1)]
        """
        return [
            Command(direction=self.direction, distance=1)
            for step in range(0, self.distance)
        ]


def to_steps(commands: list[Command]) -> list[Command]:
    """Transform a list of Commands into a list of Commands with distance 1"""
    return [step for command in commands for step in command.to_steps()]


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


def parse_command(line: str) -> Command:
    parts = line.split()
    assert len(parts) == 2, f"Could not parse {line}"
    direction = Direction.parse(parts[0])
    distance = int(parts[1])
    return Command(direction, distance)


def parse_input(lines) -> list[Command]:
    return [
        parse_command(line)
        for line in lines
        if line != ""
        # (in case we have a blank line at the end of our input)
    ]


def test_parse_input():
    assert parse_input(["R 4", "U 4", "L 3"]) == [
        Command(Direction.RIGHT, 4),
        Command(Direction.UP, 4),
        Command(Direction.LEFT, 3),
    ]


# --------
# Part 1: Simple rope movement
# --------


@dataclass
class Position:
    x: int = 0
    y: int = 0

    def is_adjacent(self, pos: "Position") -> bool:
        return abs(self.x - pos.x) <= 1 and abs(self.y - pos.y) <= 1

    def coords(self) -> tuple:
        return (self.x, self.y)

    # Allow Position to be used as a delta to another position
    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    # TODO: move this to Rope class since it bakes in assumptions about ropes?
    def rope_distance(self, pos: "Position") -> int:
        """
        The rope-distace between two positions
        This is NOT the same as manhattan distance, as rope can go diagonally.

        o-o         dx = 3   len = 3      ==  o-o-o-o
           -o-o     dy = 1                    o-o-o
                                                   -o

        o           dx = 2   len = 2
         -o         dy = 2
           -o

        o           dx = 3   len = 4
         -o         dy = 4
           -o
             -o
              o
        """
        dx = abs(self.x - pos.x)
        dy = abs(self.y - pos.y)
        return max(dx, dy)


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


@dataclass
class Rope_v1:
    """Simplistic rope movement"""

    head: Position
    tail: Position
    max_length: int = 1

    def __len__(self):
        return self.head.rope_distance(self.tail)

    def __str__(self):
        return f"({self.x}, {self.y})"

    # GK: I think I need this when trying to move the tail of the rope
    def closest_adjacent_pos(self, tail: "Position", head: "Position") -> "Position":
        """
        Find the next closest space to another position, e.g. after
        the head has moved.

        > the tail always moves one step diagonally to keep up

        Examples:

            ..H
            ..o<-- desired position
            .T.

            ...
            T..
            .oH
            ^---- desired position
        """
        if tail.is_adjacent(head):
            return tail

        dx = head.x - tail.x
        dy = head.y - tail.y

        # Because we are _always_ moving on a diagonal,
        # we don't need to apply logic to pick directions,
        # a unit vector is enough to tell us what we need.
        delta = Position(x=int(dx / abs(dx)), y=int(dy / abs(dy)))
        return tail + delta


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


def part_1(input, verbose=False):
    commands = parse_input(input)
    steps = to_steps(commands)

    rope = Rope_v1(head=Position(0, 0), tail=Position(0, 0))
    visited = set()

    for step in steps:
        rope.move_head(step)
        visited.add(rope.tail.coords())
        if verbose:
            print(f"  head: {rope.head}  tail: {rope.tail}")

    return len(visited)


def part_2(input, verbose=False):
    pass


def day_9(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
