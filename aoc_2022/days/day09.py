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
# Part 1: simple rope movement
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


@dataclass
class Position:
    x: int = 0
    y: int = 0

    def is_adjacent(self, pos: "Position") -> bool:
        return abs(self.x - pos.x) <= 1 and abs(self.y - pos.y) <= 1

    def coords(self) -> tuple:
        return (self.x, self.y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

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


def get_step_position_delta(step: Command) -> Position:
    # one unit in a step's direction.
    # Steps are assumed to have a distance of 1
    direction = step.direction
    assert step.distance == 1
    dx, dy = (0, 0)
    # structural pattern matching requires python 3.10
    match direction:
        case Direction.UP:
            dx, dy = (0, 1)
        case Direction.DOWN:
            dx, dy = (0, -1)
        case Direction.LEFT:
            dx, dy = (-1, 0)
        case Direction.RIGHT:
            dx, dy = (1, 0)
    return Position(dx, dy)


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
        unit_dx = 0 if dx == 0 else int(dx / abs(dx))  # prevent div by zero ;)
        unit_dy = 0 if dy == 0 else int(dy / abs(dy))
        delta = Position(x=unit_dx, y=unit_dy)
        return tail + delta

    def move_head(self, step: Command):
        delta = get_step_position_delta(step)
        self.head += delta
        self.move_tail_to_follow_head()

    def move_tail_to_follow_head(self):
        new_tail_pos = self.closest_adjacent_pos(self.tail, self.head)
        self.tail = new_tail_pos


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


# -----------------------------------------
# Part 2: 10 segments (H, 1, 2, 3, ... 9)
# -----------------------------------------
#
#       Rather than two knots, you now must simulate a rope consisting of ten knots.
#       One knot is still the head of the rope and moves according to the [steps].
#       Each knot further down the rope follows the knot in front of it
#       using the same rules as before.
#
# The problem statement says that the knots move "using the same rules as before",
# but the examples given seem very strange. e.g.:
#
#   == U 4 ==
#
#   ......
#   ......
#   ......
#   ....H.
#   4321..  (4 covers 5, 6, 7, 8, 9, s)
#
#   ......
#   ......
#   ....H.
#   .4321.
#   5.....  (5 covers 6, 7, 8, 9, s)
#
#   ....H.
#   ....1.
#   ..432.
#   .5....
#   6.....  (6 covers 7, 8, 9, s)
#


@dataclass
class RopeSegment(Rope_v1):
    """
    Represent a rope segment, which connects two knots of our multi-segment rope.
    Movement behavior is same as for Rope_v1
    """

    # head: my parent's tail,
    # tail: my position
    pass


class Rope_v2:
    """Multi-segment rope"""

    def __init__(self, n_knots=10):
        self.segments = [
            Rope_v1(head=Position(0, 0), tail=Position(0, 0)) for _ in range(1, n_knots)
        ]

    def move_head(self, step: Command):
        self.segments[0].move_head(step)
        prev_segment = self.segments[0]
        # For each of the other segments
        for segment in self.segments[1:]:
            segment.head = prev_segment.tail  # already moved
            segment.move_tail_to_follow_head()
            prev_segment = segment

    @property
    def tail(self):
        # tail of the last segment
        return self.segments[-1].tail


def part_2(input, verbose=False):
    commands = parse_input(input)
    steps = to_steps(commands)

    # rope = Rope_v1(head=Position(0, 0), tail=Position(0, 0))
    rope = Rope_v2(n_knots=10)
    visited = set()

    for step in steps:
        if verbose:
            print(f"--- move: {step}")
        rope.move_head(step)
        visited.add(rope.tail.coords())
        if verbose:
            for index, segment in enumerate(rope.segments):
                print(f"  {index}  head: {segment.head}  tail: {segment.tail}")

    return len(visited)


def day_9(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
