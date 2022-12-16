"""
# https://adventofcode.com/2022/day/7
"""
from typing import List
from utils.utils import get_line_items
from enum import Enum

input = list(get_line_items("aoc_2022/input/07.txt"))
toy_input: List[str] = [
    # fmt: off
    "$ cd /",
    "$ ls",
    "dir a",
    "14848514 b.txt",
    "8504156 c.dat",
    "dir d",
    "$ cd a",
    "$ ls",
    "dir e",
    "29116 f",
    "2557 g",
    "62596 h.lst",
    "$ cd e",
    "$ ls",
    "584 i",
    "$ cd ..",
    "$ cd ..",
    "$ cd d",
    "$ ls",
    "4060174 j",
    "8033020 d.log",
    "5626152 d.ext",
    "7214296 k",
    # fmt: on
]


def part_1(input, verbose=False):
    """
    Given the commands and output in the example above, you can determine that
    the filesystem looks visually like this:

        - / (dir)
          - a (dir)
            - e (dir)
              - i (file, size=584)
            - f (file, size=29116)
            - g (file, size=2557)
            - h.lst (file, size=62596)
          - b.txt (file, size=14848514)
          - c.dat (file, size=8504156)
          - d (dir)
            - j (file, size=4060174)
            - d.log (file, size=8033020)
            - d.ext (file, size=5626152)
            - k (file, size=7214296)

    ... you need to determine the total size of each directory.

    Find all of the directories with a total size of at most 100000,
    then calculate the sum of their total sizes.
    In the example above, these directories are a and e;
    the sum of their total sizes is 95437 (94853 + 584).
    (As in this example, this process can count files more than once!)
    """
    pass


def part_2(input, verbose=False):
    pass


def day_7(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
