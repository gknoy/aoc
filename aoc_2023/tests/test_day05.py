"""
# https://adventofcode.com/2023/day/5
"""
from aoc_2023.days.day05 import (
    input,
    toy_input,
    part_1,
    part_2,
    Mapping,
    MapSegment,
    ChainedMapping,
    parse_input,
)


def test_map_segment():
    a = MapSegment(50, 98, 2)
    b = MapSegment(52, 50, 48)

    assert b < a  # b's inputs are for an earlier sequence than a's inputs

    assert 98 in a
    assert 99 in a
    assert 97 not in a
    assert 100 not in a
    assert a[98] == 50
    assert a[99] == 51

    assert 49 not in b
    assert 50 in b
    assert 97 in b
    assert 98 not in b
    for k in range(50, 98):  # not including 98
        assert b[k] == k + 2


def test_mapping():
    a = MapSegment(50, 98, 2)
    b = MapSegment(52, 50, 48)

    m = Mapping("a", "b", [a, b])
    assert str(m) == "a-to-b"

    # un-mapped keys map to same destination
    assert m[-1] == -1
    assert m[1000] == 1000
    for k in range(0, 50):
        assert m[k] == k

    # b's mapped items:
    for k in range(50, 98):
        assert m[k] == k + 2
        assert m[k] == b[k]

    # a's mapped items work:
    assert m[98] == 50
    assert m[99] == 51


def test_parse_input():
    lines = [
        "seeds: 79 14 55 13",
        "",
        "seed-to-soil map:",
        "50 98 2",
        "52 50 48",
        "",
        "soil-to-fertilizer map:",
        "0 15 37",
        "37 52 2",
        "39 0 15",
    ]
    expected = (
        [79, 14, 55, 13],
        {
            "seed": Mapping("seed", "soil", [MapSegment(50, 98, 2), MapSegment(52, 50, 48)]),
            "soil": Mapping(
                "soil",
                "fertilizer",
                [
                    MapSegment(0, 15, 37),
                    MapSegment(37, 52, 2),
                    MapSegment(39, 0, 15),
                ],
            ),
        },
    )
    parsed = parse_input(lines)
    assert parsed == expected


def test_chained_mapping():
    m = ChainedMapping(
        mappings={
            "seed": Mapping("seed", "soil", [MapSegment(50, 98, 2), MapSegment(52, 50, 48)]),
            "soil": Mapping(
                "soil",
                "fertilizer",
                [
                    MapSegment(0, 15, 37),
                    MapSegment(37, 52, 2),
                    MapSegment(39, 0, 15),
                ],
            ),
        },
    )
    # (partial mapping means we don't use the full example)
    assert m[79] == 81  # Seed 79, soil 81, fertilizer 81, .... humidity 78, location 82.
    assert m[14] == 53  # Seed 14, soil 14, fertilizer 53, .... humidity 43, location 43.
    assert m[55] == 57  # Seed 55, soil 57, fertilizer 57, .... humidity 82, location 86.
    assert m[13] == 52  # Seed 13, soil 13, fertilizer 52, .... humidity 35, location 35.

    _, mappings = parse_input(toy_input)
    m = ChainedMapping(mappings=mappings)
    assert m[79] == 82  # Seed 79, soil 81, fertilizer 81, .... humidity 78, location 82.
    assert m[14] == 43  # Seed 14, soil 14, fertilizer 53, .... humidity 43, location 43.
    assert m[55] == 86  # Seed 55, soil 57, fertilizer 57, .... humidity 82, location 86.
    assert m[13] == 35  # Seed 13, soil 13, fertilizer 52, .... humidity 35, location 35.


def test_part_1_toy():
    assert part_1(toy_input) == 35


def test_part_1_real():
    assert part_1(input) == 379811651


# def test_part_2_toy():
#     assert part_2(toy_input) == "FIXME"


# def test_part_2_real():
#     assert part_2(input) == "FIXME"
