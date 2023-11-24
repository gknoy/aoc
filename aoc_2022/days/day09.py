"""
# https://adventofcode.com/2022/day/9
#
# rope movement
"""
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from utils.utils import get_line_items

input = list(get_line_items("aoc_2022/input/09.txt"))
toy_input: List[str] = [
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
    UP = "U"
    DOWN = "D"
    RIGHT = "R"
    LEFT = "L"


@dataclass
class Command:
    direction: Direction
    distance: int

    def __str__(self):
        return f"({self.direction} {self.distance})"

    def to_steps(self) -> List["Command"]:
        """
        Get a list of commands with distance 1
        e.g.  (R 4) -> [(R 1), (R 1), (R 1), (R 1)]
        """
        return [
            Command(direction=self.direction, distance=1)
            for step in range(0, self.distance)
        ]


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


directions_by_abbrev = {
    "U": Direction.UP,
    "D": Direction.DOWN,
    "R": Direction.RIGHT,
    "L": Direction.LEFT,
}


def parse_direction(s: str) -> Optional[Direction]:
    return directions_by_abbrev.get(s)


def parse_command(line: str) -> Command:
    parts = line.split()
    assert len(parts) == 2, f"Could not parse {line}"
    direction = parse_direction(parts[0])
    assert direction is not None, f"Could not parse direction from {line}"
    distance = int(parts[1])
    return Command(direction, distance)


def parse_input(lines) -> list[Command]:
    return [
        parse_command(line)
        for line in lines
        if line != ""
        # (in case we have a blank line at the end of our input)
    ]




def part_1(input, verbose=False):
    commands = parse_input(input)
    steps = [
        step
        for command in commands
        for step in command.to_steps()
    ]


def part_2(input, verbose=False):
    pass


def day_9(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
