"""
# https://adventofcode.com/2021/day/10
"""
from typing import List
from utils import get_line_items

input = list(get_line_items("input/10.txt"))
toy_input: List[str] = [
    "[({(<(())[]>[[{[]{<()<>>",
    "[(()[<>])]({[<{<<[]>>(",
    "{([(<{}[<>[]}>{[]{[(<()>",
    "(((({<>}<{<{<>}{[]{[]{}",
    "[[<[([]))<([[{}[[()]]]",
    "[{[{({}]{}}([{[{{{}}([]",
    "{<[[]]>}<{[{[{[]{()[[[]",
    "[<(<(<(<{}))><([]([]()",
    "<{([([[(<>()){}]>(<<{{",
    "<{([{{}}[<[[[<>{}]]]>[]]",
]


def fmt_error(found, expected):
    return f"Expected {expected}, but found {found} instead."


class CharStack:
    open_to_close = {
        "(": ")",
        "[": "]",
        "{": "}",
        "<": ">",
    }

    close_to_open = {
        ")": "(",
        "]": "[",
        "}": "{",
        ">": "<",
    }

    def __init__(self):
        self.stack = []

    def push(self, char):
        if char in self.open_to_close:
            self.stack.push()

    # TODO: Add score() for illegal chars

    def __len__(self):
        return len(self.stack)

def part_1(input, verbose=False):
    """
    Brace matching within each line: each line must have matched brace to be valid.
    Stop at the first incorrect closing character on each corrupted line.
    - brace-matched lines: OK
    - incomplete: OK
    - bad - give messages
    """

    # push open chars into stack, unpack when

    illegal_char_pts = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    pass


def part_2(input, verbose=False):
    """
    Brace matching s
    """

    pass


def day_10(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
