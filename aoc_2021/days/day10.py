"""
# https://adventofcode.com/2021/day/10
"""
from typing import List
from utils.utils import get_line_items

input = list(get_line_items("aoc_2021/input/10.txt"))
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
    open_to_close = {"(": ")", "[": "]", "{": "}", "<": ">"}

    close_to_open = {")": "(", "]": "[", "}": "{", ">": "<"}

    def __init__(self, verbose=False):
        self.stack = []
        self.valid = True
        self.illegal = []
        self.verbose = verbose

    def debug(self, s):
        if self.verbose:
            print(s)

    def push(self, char):
        # we're always allowed to open a new set of brackets
        if not self.valid:
            # self.illegal.append(char)
            # self.debug(f"  Ignore: {char}")
            return False

        if char in self.open_to_close:
            self.debug(f" {self.stack} ++ {char}")
            self.stack.append(char)
            return True

        # otherwise, char is a Closing bracket.
        if len(self.stack) == 0:
            self.valid = False
            self.illegal.append(char)
            self.debug(f"  Ignore: {char}")
            self.error(found=None, expected=list(self.open_to_close))
            return False

        last_open = self.stack[-1]
        expected = self.open_to_close[last_open]
        if char != expected:
            self.valid = False
            self.illegal.append(char)
            self.debug(f"  Ignore: {char}")
            self.error(found=char, expected=expected)
            return False
        else:
            popped = self.stack.pop()
            self.debug(f"popped: {popped}")
            return True

    def completion(self):
        # get the set of chars needed to complete the current
        # we know they are all OPENING characters, else they'd have
        # closed and popped an existing pattern.
        if not self.valid:
            raise Exception("Cannot complete invalid lines")

        if not self.stack:
            raise Exception("Cannot complete an empty line")

        return [self.open_to_close[c] for c in reversed(self.stack)]

    def error(self, found, expected):
        self.debug(f"Expected {expected}, but found {found} instead.")

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
    stacks = []
    for line in input:
        if verbose:
            print(f">>> Processing: {line}")
        cs = CharStack(verbose=verbose)
        for c in line:
            cs.push(c)
        stacks.append(cs)

    illegal_char_pts = {
        ")": 3,  # force black to list these vertically ;)
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    def score(stack):
        return 0 if stack.valid else illegal_char_pts[stack.illegal[0]]

    return sum(map(score, stacks))


def part_2(input, verbose=False):
    """
    Brace matching. Discard invalid lines.
    """

    # push open chars into stack, unpack when
    stacks = []
    for line in input:
        if verbose:
            print(f">>> Processing: {line}")
        cs = CharStack(verbose=verbose)
        for c in line:
            cs.push(c)
        if cs.valid:
            stacks.append(cs)

    closing_char_points = {
        ")": 1,  # force black to list these vertically ;)
        "]": 2,
        "}": 3,
        ">": 4,
    }

    def score(stack):
        score = 0
        for c in stack.completion():
            score *= 5
            score += closing_char_points[c]
        return score

    scores = list(sorted(map(score, stacks)))
    middle_score = scores[int(len(scores) / 2)]
    return middle_score


def day_10(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
