#! /usr/bin/env python
"""
#
# advent.py
#
"""
import sys

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


# -----------------------
# actually run things ...
# -----------------------

ADVENTS = {"1": one}


if __name__ == "__main__":
    for item in sys.argv[1:]:
        print(f"--- {item} ---")
        # TODO benchmarks
        print(ADVENTS[item]())
