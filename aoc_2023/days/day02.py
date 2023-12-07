"""
# https://adventofcode.com/2023/day/2
"""
from utils.utils import get_line_items

input = list(get_line_items("aoc_2023/input/02.txt"))
toy_input: list[str] = [
    # fmt: off
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    # fmt: on
]

# ----------------------------------
# Part 1
# ----------------------------------
# pull N of each color, and then _put them back_
# Which games would have been possible if the bag contained only
# 12 red cubes, 13 green cubes, and 14 blue cubes?
#
# If you add up the IDs of the games that would have been possible, you get 8

Pull = dict[str, int]
Game = dict[str, (int | list[Pull])]  # {1: [{b: 3, r: 4}, {r: 1, g: 2, b: 6}]}


def parse_cube_count(item: str) -> tuple[str, int]:
    n, c = item.split(" ")
    return (c[0], int(n))


def parse_pull(pull_str: str) -> Pull:
    items = pull_str.split(", ")
    return dict(parse_cube_count(item.strip()) for item in items)


def parse_game(line: str) -> Game:
    # line: semicolon-separated list of pulls
    #       pulls are comma-separated segments of "{color} {count}"
    game_tag, raw_pulls = list(line.split(":"))
    game_id = int(game_tag.split(" ")[1])
    pulls = raw_pulls.split("; ")
    return {"id": game_id, "pulls": [parse_pull(pull.strip()) for pull in pulls]}


def game_possible(game: Game, constraints: Pull) -> bool:
    pulls = game["pulls"]
    return all(pull_possible(pull, constraints) for pull in pulls)


def pull_possible(pull: Pull, constraints: Pull) -> bool:
    return all(constraints.get(c, 0) >= n for c, n in pull.items())


def filter_possible_games(games, constraints: Pull) -> list[Game]:
    # Return only the games where all of the pulls are <= constraint counts
    return [game for game in games if game_possible(game, constraints)]


def part_1(input, verbose=False):
    # which games are possible with these constraints?
    # 12 red cubes, 13 green cubes, and 14 blue cubes
    constraints = {"r": 12, "g": 13, "b": 14}
    games = [parse_game(line) for line in input]
    filtered_games = filter_possible_games(games, constraints)
    return sum(game["id"] for game in filtered_games)


# ----------------------------------
# Part 2
# ----------------------------------
# sum of powers of pulls


def power(pull: Pull) -> int:
    return pull.get("r", 0) * pull.get("g", 0) * pull.get("b", 0)


def min_possible_counts(game: Game) -> Pull:
    """Find the smallest number of cubes needed to satisfy all pulls"""
    # this is the same of max(r), max(g), max(b) for all pulls in the game
    maxes = {"r": 0, "g": 0, "b": 0}
    for pull in game["pulls"]:
        for c in pull:
            maxes[c] = max(pull[c], maxes[c])
    return maxes


def part_2(input, verbose=False):
    # What is the fewest number of cubes of each color
    # that could have been in the bag to make the game possible?
    # The power(pull) == count of red, green, and blue cubes multiplied together.
    # The power of the minimum set of cubes in game 1 is 48.
    # In games 2-5 it was 12, 1560, 630, and 36, respectively.
    # Adding up these five powers produces the sum 2286.

    games = [parse_game(line) for line in input]
    min_powers_per_pull = [power(min_possible_counts(game)) for game in games]
    return sum(min_powers_per_pull)


def day_2(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
