"""
# https://adventofcode.com/2022/day/6
"""
from aoc_2022.days.day06 import (
    input,
    toy_input,
    part_1,
    part_2,
    find_packet_start,
    find_message_start,
)


def test_find_packet_start():
    test_data = {
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb": 7,  # toy input ;)
        "bvwbjplbgvbhsrlpgdmjqwftvncz": 5,
        "nppdvjthqldpwncqszvftbrmjlhg": 6,
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": 10,
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": 11,
    }
    for stream, expected in test_data.items():
        assert expected == find_packet_start(stream)


def test_find_message_start():
    test_data = {
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb": 19,
        #     ^^^^^^^^^^^^^^
        "bvwbjplbgvbhsrlpgdmjqwftvncz": 23,
        "nppdvjthqldpwncqszvftbrmjlhg": 23,
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": 29,
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": 26,
    }
    for stream, expected in test_data.items():
        assert expected == find_message_start(stream)


def test_part_1_toy():
    assert part_1(toy_input) == 7


def test_part_1_real():
    assert part_1(input) == 1816


def test_part_2_toy():
    assert part_2(toy_input) == 19


def test_part_2_real():
    assert part_2(input) == 2625
