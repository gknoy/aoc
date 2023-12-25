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
        PartNumber(value=13, start=(6, 1), end=(6, 3)),
        Symbol(name="+", start=(6, 5), end=(6, 6)),
        PartNumber(value=58, start=(6, 7), end=(6, 9)),
    ]
    assert parse_line(line, 6) == expected


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
            PartNumber(value=13, start=(0, 1), end=(0, 3)),
            Symbol(name="+", start=(0, 5), end=(0, 6)),
            PartNumber(value=58, start=(0, 7), end=(0, 9)),
        ],
    ]
    assert get_at_position(grid, (0, 2)) == PartNumber(value=13, start=(0, 1), end=(0, 3))
    assert get_at_position(grid, (0, 5)) == Symbol(name="+", start=(0, 5), end=(0, 6))
    assert get_at_position(grid, (0, 8)) == PartNumber(value=58, start=(0, 7), end=(0, 9))


def test_get_adjacent_parts():
    #   "467..114..",
    #   "...*......",  # <<< 35, 467 are both adjacent to star
    #   "..35..633.",
    grid = [
        [
            PartNumber(value=467, start=(0, 0), end=(0, 3)),
            PartNumber(value=114, start=(0, 5), end=(0, 8)),
        ],
        [Symbol(start=(1, 3), end=(1, 4), name="*")],
        [
            PartNumber(start=(2, 2), end=(2, 4), value=35),
            PartNumber(start=(2, 6), end=(2, 9), value=633),
        ],
    ]
    adj_parts = get_adjacent_parts(grid, (1, 3))
    assert len(adj_parts) == 2
    assert set(adj_parts) == set(
        [
            PartNumber(start=(0, 0), end=(0, 3), value=467),
            PartNumber(start=(2, 2), end=(2, 4), value=35),
        ]
    )


def test_find_part_numbers():
    #   "467..114..",
    #   "...*......",  # <<< 35, 467 are both adjacent to star
    #   "..35..633.",
    grid = [
        [
            PartNumber(start=(0, 0), end=(0, 3), value=467),
            PartNumber(start=(0, 5), end=(0, 8), value=114),
        ],
        [Symbol(start=(1, 3), end=(1, 4), name="*")],
        [
            PartNumber(start=(2, 2), end=(2, 4), value=35),
            PartNumber(start=(2, 6), end=(2, 9), value=633),
        ],
    ]
    parts = list(find_part_numbers(grid))
    assert len(parts) == 2
    assert set(parts) == set(
        [
            PartNumber(start=(0, 0), end=(0, 3), value=467),
            PartNumber(start=(2, 2), end=(2, 4), value=35),
        ]
    )


def test_find_pns_two():
    lines = [
        # fmt: off
        ".......................661.........................485..565.......344.......325.....................................841.....725.............",
        "....*609..131................512.......................*................536*..............462/..-...60..424.........@....$.*................",
        ".316.........*.......39..................@.630......377........919...........98................789..*..*..............788..2.......=..564...",
        "...........431...535...*...............622.-..../.................*..........*.......682...........108.116....@...-...............299.......",
        ".....................428.....378...844.........416...............586.537=..27..........*......$..............871...331..................492.",
        "...878....390....%..............*.*...................739.496=.................867......867..867.........................344......487.../...",
        "...../.....*...558........@..535...644..................+.........404..605.......*................................%.....*...................",
        "........................381............729..726....578........10...*..........818..............................929....934..........119......",
        ".53....31..........734-..........847*.................#.........*...........#............217............/..321....................*.........",
        ".......=.............................509.315.654.................60.........925.747*559..*.....430....226..*...................290...848=...",
        "..........=.......546......664..507......../....#.......337.............................94........=.........359....528*996..................",
        ".....351...638.......*.............*433............337.....................226...859........../............................378..............",
        # fmt: on
    ]
    part_numbers = list(find_part_numbers(parse_grid(lines)))
    # part_numbers_set = set(part_numbers)
    values = [part.value for part in part_numbers]
    expected = [
        # in order by symbol encountered
        # fmt: off
        # (no symbols in first row)
        316, 609, 377, 565, 536, 325, 462, 789, 841, 788, 2, 725,
        131, 431, 622, 108, 60, 116, 424, 299,
        39, 428, 630, 416, 919, 586, 27, 98, 871, 331,
        537, 682, 867, 867,
        558, 378, 535, 844, 644, 496, 492,
        878, 390, 381, 739, 818, 867, 929, 934, 344,
        404,
        734, 847, 509, 578, 10, 60, 925, 226, 290, 119,
        31, 747, 559, 94, 217, 321, 359, 848,
        638, 315, 654, 430, 528, 996,
        546, 507, 433,
        # fmt: on
    ]
    sorted_values  = list(sorted(values))
    sorted_expected = list(sorted(expected))
    assert sorted_values == sorted_expected
    # assert values == expected


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
            PartNumber(start=(0, 0), end=(0, 3), value=467),
            PartNumber(start=(0, 5), end=(0, 8), value=114),
        ],
        [Symbol(start=(1, 3), end=(1, 4), name="*")],
        [
            PartNumber(start=(2, 2), end=(2, 4), value=35),
            PartNumber(start=(2, 6), end=(2, 9), value=633),
        ],
        [Symbol(start=(3, 6), end=(3, 7), name="#")],
        [
            PartNumber(start=(4, 0), end=(4, 3), value=617),
            Symbol(start=(4, 3), end=(4, 4), name="*"),
        ],
        [
            Symbol(start=(5, 5), end=(5, 6), name="+"),
            PartNumber(start=(5, 7), end=(5, 9), value=58),
        ],
        [PartNumber(start=(6, 2), end=(6, 5), value=592)],
        [PartNumber(start=(7, 6), end=(7, 9), value=755)],
        [Symbol(start=(8, 3), end=(8, 4), name="$"), Symbol(start=(8, 5), end=(8, 6), name="*")],
        [
            PartNumber(start=(9, 1), end=(9, 4), value=664),
            PartNumber(start=(9, 5), end=(9, 8), value=598),
        ],
    ]

    assert parse_grid(toy_input) == expected


def test_part_1_toy():
    assert part_1(toy_input) == 4361


# def test_part_1_real():
#     answer = part_1(input)
#     assert answer > 517752  # too low apparently, but I can't figure out why
#     assert part_1(input) == "FIXME"


# def test_part_2_toy():
#     assert part_2(toy_input) == "FIXME"


# def test_part_2_real():
#     assert part_2(input) == "FIXME"
