"""
# https://adventofcode.com/2023/day/2
"""
from aoc_2023.days.day02 import input, toy_input, part_1, part_2, parse_game, parse_pull


def test_parse_pull():
    assert parse_pull("1 red, 2 green, 6 blue") == {"r": 1, "g": 2, "b": 6}


def test_parse_game():
    game = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    assert parse_game(game) == {
        "id": 1,
        "pulls": [
            {"b": 3, "r": 4},
            {"r": 1, "g": 2, "b": 6},
            {"g": 2},
        ],
    }


def test_part_1_toy():
    assert part_1(toy_input) == 8


def test_part_1_real():
    assert part_1(input) == 2776


def test_part_2_toy():
    assert part_2(toy_input) == 2286


def test_part_2_real():
    assert part_2(input) == 68638
