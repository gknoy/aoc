"""
# https://adventofcode.com/2023/day/4
"""
from dataclasses import dataclass
from utils.utils import get_line_items

input = list(get_line_items("aoc_2023/input/04.txt"))
toy_input: list[str] = [
    # fmt: off
    #        (winning)      | (your card numbers)
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
    # fmt: on
]

# ---------------------
# Part 1: Scratchcards
# ---------------------
# first match makes the card worth one point
# each match after the first doubles the point value of that card


@dataclass
class Card:
    name: str = ""  # e.g. "Card 1"
    numbers: tuple = ()
    winning: tuple = ()
    score: int = 0


def _strip(items: list[str]) -> list[str]:
    return [item.strip() for item in items]


def geometric_score(winning: list[int], numbers: list[int], base: int = 2) -> int:
    matches = [item for item in numbers if item in winning]
    if len(matches) == 0:
        return 0
    # 1 match: 1 point (2^0), double each extra
    return pow(base, len(matches) - 1)


def parse_line(line: str) -> Card:
    name, rest = _strip(line.split(":"))
    winning_raw, numbers_raw = _strip(rest.split("|"))
    winning = [int(item) for item in winning_raw.split()]
    numbers = [int(item) for item in numbers_raw.split()]
    score = geometric_score(winning, numbers, 2)
    return Card(name=name, numbers=numbers, winning=winning, score=score)


def part_1(input, verbose=False):
    cards = [parse_line(line) for line in input]
    return sum(card.score for card in cards)


def part_2(input, verbose=False):
    pass


def day_4(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
