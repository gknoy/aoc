"""
# https://adventofcode.com/2021/day/4
"""
import time

from collections import defaultdict
from utils import get_line_items

input = list(get_line_items("input/04.txt"))
toy_input = [
    "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1",
    "",
    "22 13 17 11  0",  # board 1
    " 8  2 23  4 24",
    "21  9 14 16  7",
    " 6 10  3 18  5",
    " 1 12 20 15 19",
    "",
    " 3 15  0  2 22",
    " 9 18 13 17  5",
    "19  8  7 25 23",
    "20 11 10 24  4",
    "14 21 16 12  6",
    "",
    "14 21 17 24  4",
    "10 16 15  9 19",
    "18  8 23 26 20",
    "22 11 13  6  5",
    " 2  0 12  3  7",
]

BOLD = "\033[1m"
CLEAR = "\033[0m"


class Board:
    done: bool
    called: dict
    rows: list
    score: int

    def __init__(self, board_lines):
        # parse board lines into rows/cols
        self.done = False
        self.called = defaultdict(bool)
        self.rows = self.parse_rows(board_lines)
        self.cols = [[row[i] for row in self.rows] for i in range(len(self.rows[0]))]
        self.score = 0
        assert len(self.rows) == len(self.cols)

    def __str__(self):
        """Pretty-print with selected numbers in bold"""
        row_strings = [
            "".join([self.render_item(item) for item in row]) for row in self.rows
        ] + [f"  score: {self.score}\n"]
        return "\n".join(row_strings)

    def render_item(self, number):
        if self.called[number]:
            return f"{BOLD}{number:3}{CLEAR}"
        return f"{number:3}"

    def call(self, number):
        if self.done:
            return self.score
        self.called[number] = True
        if self.any_all_called(self.rows) or self.any_all_called(self.cols):
            self.done = True
            self.score = self.calc_score(number)
        return self.score

    def parse_rows(self, lines):
        return [[int(item) for item in line.split()] for line in lines]

    def all_items_called(self, items):
        # any item in a row or col
        return all(self.called[item] for item in items)

    def any_all_called(self, rows_or_cols):
        return any(self.all_items_called(item) for item in rows_or_cols)

    def uncalled_numbers(self):
        return [
            item
            # this always looks weird to me
            for row in self.rows
            for item in row
            if not self.called[item]
        ]

    def calc_score(self, last_called):
        if self.done:
            return sum(self.uncalled_numbers()) * last_called
        return 0


def get_boards(input):
    boards = []
    lines = []

    for line in input:
        if line == "":
            if lines:
                boards.append(Board(lines))
                lines = []
            continue
        lines.append(line)

    if lines:
        boards.append(Board(lines))

    return boards


def part_1(input, verbose=False):
    """
    Play bingo with input draws + boards
    """
    calls = list(map(int, input[0].split(",")))
    boards = get_boards(input[1:])

    for number in calls:
        scores = [board.call(number) for board in boards]
        for index, score in enumerate(scores):
            if score > 0:
                if verbose:
                    print("Winning board:")
                    print(boards[index])
                assert score == boards[index].score
                return score


def part_2(input, verbose=False):
    """
    Find the LAST winning board
    """
    calls = list(map(int, input[0].split(",")))
    all_boards = get_boards(input[1:])
    boards = [b for b in all_boards]

    for number in calls:
        if verbose:
            print(f">>> Called: {number}")
        scores = [board.call(number) for board in boards]
        boards_to_drop = []
        for index, score in enumerate(scores):
            if score > 0:
                boards_to_drop.append(index)
                if len(boards) == 1:
                    # this is the last one!
                    if verbose:
                        print("Last winning board:")
                        print(boards[index])
                    assert score == boards[index].score
                    return score

        # Drop any boards that were finished
        if boards_to_drop:
            if verbose:
                print(f"    Dropping boards {boards_to_drop}")
                for index in boards_to_drop:
                    print(boards[index])

            last_dropped = boards[boards_to_drop[-1]]

            # drop boards that had scores:
            boards = [
                board for board in boards if board.score == 0
            ]
            if len(boards) == 0:
                # none of the boards are left, so use the one that scored LAST:
                if verbose:
                    print("   All boards dropped. Last board:")
                    print(last_dropped)
                return last_dropped.score

        if verbose:
            print(f"    {len(boards)} boards remaining\n")
            time.sleep(1)


def day_4(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
