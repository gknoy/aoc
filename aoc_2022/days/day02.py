"""
# https://adventofcode.com/2022/day/2
#
# Rock paper scissors tourney
#
"""
import pytest

from enum import Enum
from typing import Callable, Dict, List, Tuple
from utils.utils import get_line_items

input = list(get_line_items("aoc_2022/input/02.txt"))
toy_input: List[str] = [
    # fmt: off
    "A Y",
    "B X",
    "C Z",
    # fmt: on
]


class MoveType(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Move:
    def __init__(self, type, beats, loses_to):
        self.type = type
        self.beats = beats
        self.loses_to = loses_to

    def __repr__(self):
        return f"<Move {self.type.name}>"

    def __str__(self):
        return self.type.name

    def __eq__(self, other):
        return self.type == other.type

    def __lt__(self, other):
        return self.loses_to == other.type

    def __gt__(self, other):
        return self.beats == other.type


# canonical moves
R = Move(MoveType.ROCK, beats=MoveType.SCISSORS, loses_to=MoveType.PAPER)
P = Move(MoveType.PAPER, beats=MoveType.ROCK, loses_to=MoveType.SCISSORS)
S = Move(MoveType.SCISSORS, beats=MoveType.PAPER, loses_to=MoveType.ROCK)
# not shotgun ;)


canonical_moves = {MoveType.ROCK: R, MoveType.PAPER: P, MoveType.SCISSORS: S}


def score(a: Move, b: Move) -> int:
    """
    The score for a single round is
    the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors)
    plus the score for the outcome of the round
    (0 if you lost, 3 if the round was a draw, and 6 if you won)"""
    score = a.type.value
    if a == b:
        score += 3
    elif a < b:
        score += 0
    else:
        assert a > b
        score += 6
    return score


@pytest.mark.parametrize(
    "move,opponent,eq,win,lose,points",
    [
        # equal things
        [R, R, True, False, False, 3 + 1],
        [P, P, True, False, False, 3 + 2],
        [S, S, True, False, False, 3 + 3],
        # wins
        [R, S, False, True, False, 6 + 1],
        [P, R, False, True, False, 6 + 2],
        [S, P, False, True, False, 6 + 3],
        # losses
        [R, P, False, False, True, 0 + 1],
        [P, S, False, False, True, 0 + 2],
        [S, R, False, False, True, 0 + 3],
    ],
)
def test_score(move, opponent, eq, win, lose, points):
    assert eq == (move == opponent)
    assert lose == (move < opponent)
    assert win == (move > opponent)
    assert points == score(move, opponent)


def decode_move(
    line: str,
    opponent_move_encoding: Dict[str, Move],
    move_picker_map: Dict[str, Callable],
) -> Tuple[Move, Move]:
    # e.g. "B Y"
    a, b = line.split(" ")
    opp_move = opponent_move_encoding[a]
    my_move = move_picker_map[b](opp_move)
    return (opp_move, my_move)


def get_move_cheatsheet(
    input: List[str],
    opponent_move_encoding: Dict[str, Move],
    move_picker_map: Dict[str, Callable],
) -> List[Tuple[Move, Move]]:
    return [
        decode_move(line, opponent_move_encoding, move_picker_map) for line in input
    ]


def part_1(input, verbose=False):
    """
    Test elf's encrypted strategy:

        "The first column is what your opponent is going to play:
        A for Rock, B for Paper, and C for Scissors. The second column--"

    -> A,B,C are RPS
    -> We assume that X,Y,Z are R,P,S

    For example, suppose you were given the following strategy guide:

    A Y
    B X
    C Z

    This strategy guide predicts and recommends the following:

    R1:
        your opponent will choose Rock (A), and you should choose Paper (Y).
        This ends in a win for you with a score of 8 (2 because you chose Paper + 6 because you won).

    R2:
        your opponent will choose Paper (B), and you should choose Rock (X).
        This ends in a loss for you with a score of 1 (1 + 0).

    R3: The third round is a draw with both players choosing Scissors,
    giving you a score of 3 + 3 = 6.
    In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

    What would your total score be if everything goes exactly according to your strategy guide?
    """
    opp_move_encoding = {"A": R, "B": P, "C": S}
    # for part 1, assume X,Y,Z are R,P,S.  I bet in Part 2 we have to figure which is best
    move_pickers = {"X": lambda move: R, "Y": lambda move: P, "Z": lambda move: S}

    cheatsheet = get_move_cheatsheet(input, opp_move_encoding, move_pickers)
    return sum(score(my_move, opp_move) for opp_move, my_move in cheatsheet)


def part_2(input, verbose=False):
    """
    X means you need to lose,
    Y means you need to end the round in a draw, and
    Z means you need to win. Good luck!"
    """
    opp_move_encoding = {"A": R, "B": P, "C": S}
    move_pickers = {
        "X": lambda opp_move: canonical_moves[opp_move.beats],
        "Y": lambda opp_move: canonical_moves[opp_move.type],
        "Z": lambda opp_move: canonical_moves[opp_move.loses_to],
    }

    cheatsheet = get_move_cheatsheet(input, opp_move_encoding, move_pickers)
    return sum(score(my_move, opp_move) for opp_move, my_move in cheatsheet)


def day_2(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
