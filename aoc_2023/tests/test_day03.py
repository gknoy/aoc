"""
# https://adventofcode.com/2023/day/3
"""
from aoc_2023.days.day03 import (
    input,
    toy_input,
    part_1,
    part_2,
    parse_line,
    parse_grid,
    PartNumber,
    Symbol,
    get_adjacent_positions,
    get_at_position,
    get_adjacent_parts,
    find_part_numbers,
)


def test_parse_line():
    line = ".13..+.58."
    #       0123456789
    expected = [
        PartNumber(value=13, start=1, end=3),
        Symbol(name="+", start=5, end=6),
        PartNumber(value=58, start=7, end=9),
    ]
    assert parse_line(line) == expected


def test_get_adjacent_positions():
    assert get_adjacent_positions((3, 4)) == [
        # fmt: off
        (2, 3), (2, 4), (2, 5),
        (3, 3),         (3, 5),
        (4, 3), (4, 4), (4, 5),
        # fmt: on
    ]


def test_get_at_position():
    grid = [
        [
            PartNumber(value=13, start=1, end=3),
            Symbol(name="+", start=5, end=6),
            PartNumber(value=58, start=7, end=9),
        ],
    ]
    assert get_at_position(grid, (0, 2)) == PartNumber(value=13, start=1, end=3)
    assert get_at_position(grid, (0, 5)) == Symbol(name="+", start=5, end=6)
    assert get_at_position(grid, (0, 8)) == PartNumber(value=58, start=7, end=9)


def test_get_adjacent_parts():
    #   "467..114..",
    #   "...*......",  # <<< 35, 467 are both adjacent to star
    #   "..35..633.",
    grid = [
        [
            PartNumber(value=467, start=0, end=3),
            PartNumber(value=114, start=5, end=8),
        ],
        [Symbol(start=3, end=4, name="*")],
        [
            PartNumber(start=2, end=4, value=35),
            PartNumber(start=6, end=9, value=633),
        ],
    ]
    adj_parts = get_adjacent_parts(grid, (1, 3))
    assert len(adj_parts) == 2
    assert set(adj_parts) == set(
        [
            PartNumber(value=467, start=0, end=3),
            PartNumber(start=2, end=4, value=35),
        ]
    )


def test_find_part_numbers():
    #   "467..114..",
    #   "...*......",  # <<< 35, 467 are both adjacent to star
    #   "..35..633.",
    grid = [
        [
            PartNumber(value=467, start=0, end=3),
            PartNumber(value=114, start=5, end=8),
        ],
        [Symbol(start=3, end=4, name="*")],
        [
            PartNumber(start=2, end=4, value=35),
            PartNumber(start=6, end=9, value=633),
        ],
    ]
    parts = list(find_part_numbers(grid))
    assert len(parts) == 2
    assert set(parts) == set(
        [
            PartNumber(value=467, start=0, end=3),
            PartNumber(start=2, end=4, value=35),
        ]
    )


def test_find_pns_two():
    lines = [
        # fmt: off
        ".......................661.........................485..565.......344.......325.....................................841.....725.............",
        "....*609..131................512.......................*................536*..............462/..-...60..424.........@....$.*................",
        ".316.........*.......39..................@.630......377........919...........98................789..*..*..............788..2.......=..564...",
        # fmt: on
    ]
    part_numbers = list(find_part_numbers(parse_grid(lines)))
    numbers = [part.value for part in part_numbers]
    assert set(numbers) == {316, 609, 131, 377, 565, 536, 325, 462, 789, 60, 424, 841, 788, 2, 725}


def test_parse_grid():
    #   "467..114..",
    #   "...*......",
    #   "..35..633.",
    #   "......#...",
    #   "617*......",
    #   ".....+.58.",
    #   "..592.....",
    #   "......755.",
    #   "...$.*....",
    #   ".664.598..",
    expected = [
        [
            PartNumber(value=467, start=0, end=3),
            PartNumber(value=114, start=5, end=8),
        ],
        [Symbol(start=3, end=4, name="*")],
        [
            PartNumber(start=2, end=4, value=35),
            PartNumber(start=6, end=9, value=633),
        ],
        [Symbol(start=6, end=7, name="#")],
        [PartNumber(start=0, end=3, value=617), Symbol(start=3, end=4, name="*")],
        [
            Symbol(start=5, end=6, name="+"),
            PartNumber(start=7, end=9, value=58),
        ],
        [
            PartNumber(start=2, end=5, value=592),
        ],
        [
            PartNumber(start=6, end=9, value=755),
        ],
        [
            Symbol(start=3, end=4, name="$"),
            Symbol(start=5, end=6, name="*"),
        ],
        [
            PartNumber(start=1, end=4, value=664),
            PartNumber(start=5, end=8, value=598),
        ],
    ]

    assert parse_grid(toy_input) == expected


def test_part_1_toy():
    assert part_1(toy_input) == 4361


def test_part_1_real():
    answer = part_1(input)
    assert answer > 517752  # too low apparently, but I can't figure out why
    assert part_1(input) == "FIXME"


# def test_part_2_toy():
#     assert part_2(toy_input) == "FIXME"


# def test_part_2_real():
#     assert part_2(input) == "FIXME"
