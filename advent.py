#! /usr/bin/env python
"""
#
# advent.py
#
"""
import sys
from dataclasses import dataclass

# ----------------------
# advent infrastructure
# ----------------------


def get_line_items(fname):
    with open(fname) as f:
        return (item.strip() for item in f.readlines())


# ----------------------
# advent problems
# ----------------------


def one():
    """
    https://adventofcode.com/2021/day/1
    """
    measurements = [int(item) for item in get_line_items("input/1.txt")]
    # toy input:
    # measurements = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

    def count_increasing_items(items):
        return sum(
            1
            for index, item in enumerate(items)
            if (index > 0 and items[index] > items[index - 1])
        )

    def part_1():
        """
        Count how many times measurement is larger than previous measurement
        """
        return count_increasing_items(measurements)

    def part_2():
        """
        Count increasing sums of N-measurement windows in the input
        """

        def window_slicer(size):
            # return a sliding window slicer
            def slicer(index, items):
                return items[index : index + size]

            return slicer

        window_size = 3
        slicer = window_slicer(window_size)

        windows = [
            slicer(index, measurements)
            for index in range(len(measurements) - window_size + 1)
        ]

        sliding_window_sums = [sum(window) for window in windows]
        return count_increasing_items(sliding_window_sums)

    return [part_1(), part_2()]


def two():
    """
    Control a submarine :D
    https://adventofcode.com/2021/day/2
    """
    commands = [item for item in get_line_items("input/2.txt")]
    # toy input:
    # commands = ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]

    class Vehicle:
        def position(self):
            raise NotImplementedError()

        def autonav(self, commands):
            for command in commands:
                self.nav(command)

        def nav(self, command):
            direction, magnitude = command.split()
            magnitude = float(magnitude)

            op = getattr(self, direction, None)
            if op is None:
                raise NotImplementedError(f"{direction} not supported")

            op(magnitude)

    def part_1():
        """
        Calculate the horizontal position and depth you would have after following the planned course.
        What do you get if you multiply your final horizontal position by your final depth?
        """

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

        sub = Sub(x=0, depth=0)
        sub.autonav(commands)

        return [sub.position(), sub.x * sub.depth]

    def part_2():
        """
        - down X increases your aim by X units.
        - up X decreases your aim by X units.
        - forward X does two things:
            - It increases your horizontal position by X units.
            - It increases your depth by your aim multiplied by X.
        """

        @dataclass
        class AimingSub(Vehicle):
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

        sub = AimingSub(x=0, depth=0, aim=0)
        sub.autonav(commands)

        return [sub.position(), sub.x * sub.depth]

    return [part_1(), part_2()]


# -----------------------
# actually run things ...
# -----------------------

ADVENTS = {"1": one, "2": two}


if __name__ == "__main__":
    for item in sys.argv[1:]:
        print(f"--- {item} ---")
        # TODO benchmarks
        print(ADVENTS[item]())
