"""
# Control a submarine :D
#
# https://adventofcode.com/2021/day/2
"""
from dataclasses import dataclass

from utils.utils import get_line_items


commands = [item for item in get_line_items("aoc_2021/input/02.txt")]
toy_commands = ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]


class Vehicle:
    def position(self):
        raise NotImplementedError()

    def autonav(self, commands):
        for command in commands:
            self.nav(command)

    def nav(self, command):
        direction, magnitude = command.split()
        magnitude = int(magnitude)

        op = getattr(self, direction, None)
        if op is None:
            raise NotImplementedError(f"{direction} not supported")

        op(magnitude)


@dataclass
class Sub(Vehicle):
    x: int
    depth: int

    def position(self):
        return {"x": self.x, "depth": self.depth}

    def forward(self, x):
        self.x += x

    def up(self, x):
        self.depth = max(0, self.depth - x)

    def down(self, x):
        self.depth += x


@dataclass
class AimingSub(Vehicle):
    """
    - down X increases your aim by X units.
    - up X decreases your aim by X units.
    - forward X does two things:
        - It increases your horizontal position by X units.
        - It increases your depth by your aim multiplied by X.
    """

    x: int
    depth: int
    aim: int  # amount that we are aiming DOWNWARD

    def position(self):
        return {"x": self.x, "depth": self.depth, "aim": self.aim}

    def forward(self, x):
        self.x += x
        self.depth = max(0, self.depth + (self.aim * x))

    def up(self, x):
        # nose up
        self.aim -= x

    def down(self, x):
        # nose down
        self.aim += x


def part_1(commands, verbose=False):
    """
    Calculate the horizontal position and depth you would have after following the planned course.
    What do you get if you multiply your final horizontal position by your final depth?
    """
    sub = Sub(x=0, depth=0)
    sub.autonav(commands)

    return sub.x * sub.depth


def part_2(commands, verbose=False):
    sub = AimingSub(x=0, depth=0, aim=0)
    sub.autonav(commands)
    return sub.x * sub.depth


def day_2(use_toy_data=False, verbose=False):
    data = toy_commands if use_toy_data else commands
    return [part_1(data, verbose), part_2(data, verbose)]
