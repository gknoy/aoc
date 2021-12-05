"""
# https://adventofcode.com/2021/day/1
"""
from utils import get_line_items

measurements = [int(item) for item in get_line_items("input/01.txt")]
toy_measurements = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


def count_increasing_items(items):
    return sum(
        1
        for index, item in enumerate(items)
        if (index > 0 and items[index] > items[index - 1])
    )


def part_1(measurements, verbose=False):
    """
    Count how many times measurement is larger than previous measurement
    """
    return count_increasing_items(measurements)


def part_2(measurements, verbose=False):
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


def day_1(use_toy_data=False, verbose=False):
    data = toy_measurements if use_toy_data else measurements
    return [part_1(data, verbose), part_2(data, verbose)]
