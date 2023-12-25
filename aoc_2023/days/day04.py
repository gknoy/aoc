"""
# https://adventofcode.com/2023/day/4
"""
from dataclasses import dataclass
from typing import Callable
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
    index: int = 0

    def get_index(self):
        return


def _strip(items: list[str]) -> list[str]:
    return [item.strip() for item in items]


def geometric_score(winning: list[int], numbers: list[int], base: int = 2) -> int:
    matches = [item for item in numbers if item in winning]
    if len(matches) == 0:
        return 0
    # 1 match: 1 point (2^0), double each extra
    return pow(base, len(matches) - 1)


def parse_line(line: str, calc_score: Callable) -> Card:
    name, rest = _strip(line.split(":"))
    winning_raw, numbers_raw = _strip(rest.split("|"))
    winning = [int(item) for item in winning_raw.split()]
    numbers = [int(item) for item in numbers_raw.split()]
    score = calc_score(winning, numbers)
    # cards start at "Card 1", but array is zero indexed
    card_index = int(name.split()[1]) - 1
    return Card(name=name, numbers=numbers, winning=winning, score=score, index=card_index)


def part_1(input, verbose=False):
    cards = [parse_line(line, geometric_score) for line in input]
    return sum(card.score for card in cards)


# ---------------------
# Part 2
# ---------------------
# There's no such thing as "points". Instead,
# scratchcards only cause you to win more scratchcards equal to the number of winning numbers you have.
#
# You win copies of the scratchcards below the winning card equal to the number of matches.
# If card 10 were to have 5 matching numbers,
# you would win one copy each of cards 11, 12, 13, 14, and 15.
#
# Copies: scored normally, have the same card number as the card they copied.
# If you win a copy of card 10 and it has 5 matching numbers,
# it would then win a copy of the same cards that the original card 10 won
#
toy_input_2: list[str] = [
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


def count_winning_cards(winning, numbers) -> int:
    # we win as many cards as we have matches
    matches = [item for item in numbers if item in winning]
    return len(matches)


def get_card_reward(cards: list[Card], card_index: int, next_count) -> list[Card]:
    return cards[card_index + 1 : card_index + next_count + 1]


def part_2(input, verbose=False):
    """
    Including the original set of scratchcards,
    how many total scratchcards do you end up with?
    - count all, not just winners
    """
    original_cards = [parse_line(line, count_winning_cards) for line in input]

    # it doesn't matter the ORDER in which we process cards, as they will win the same copies (by number/name)
    cards = list(original_cards)
    count = 0
    while len(cards):
        # Expectation: order doesn't matter since rewards are based on card identity
        card = cards.pop()  # takes from end of deck
        count += 1
        winnings = get_card_reward(original_cards, card.index, card.score)
        for card in winnings:
            cards.append(card)
    return count


def day_4(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
