"""
# https://adventofcode.com/2023/day/5
"""
from aoc_2023.days.day05 import input, toy_input, part_1, part_2, Mapping, MapSegment


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

    m = Mapping([a, b])
    assert m.map_segments == [b, a]  # sorted but likeley not needed to be

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


# def test_part_1_toy():
#     assert part_1(toy_input) == 35


# def test_part_1_real():
#     assert part_1(input) == "FIXME"


# def test_part_2_toy():
#     assert part_2(toy_input) == "FIXME"


# def test_part_2_real():
#     assert part_2(input) == "FIXME"
