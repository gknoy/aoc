"""
# https://adventofcode.com/2022/day/6
"""
from typing import List, Sequence
from utils.utils import get_line_items

input = list(get_line_items("aoc_2022/input/06.txt"))
toy_input: List[str] = [
    # fmt: off
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
    # fmt: on
]


def window(index: int, n: int, stream: Sequence):
    return stream[index: index + n]


def is_packet(chars, packet_len=4):
    return len(chars) == packet_len and len(set(chars)) == packet_len


def find_packet_end(packet_len, stream: Sequence) -> str:
    for index in range(len(stream)):
        if is_packet(window(index, packet_len, stream)):
            return index + packet_len
    raise EOFError


def test_find_packet_end():
    test_data = {
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb": 7,  # toy input ;)
        "bvwbjplbgvbhsrlpgdmjqwftvncz": 5,
        "nppdvjthqldpwncqszvftbrmjlhg": 6,
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": 10,
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": 11,
    }
    for stream, expected in test_data.items():
        assert expected == find_packet_end(4, stream)


def part_1(input, verbose=False):
    """
    Detect a start-of-packet marker in the datastream.
    In the protocol being used by the Elves, the start of a packet is indicated by
    a sequence of four characters that are all different.

        bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 5
        ^^^^ has duplicate
         ^^^^ no duplixate
        nppdvjthqldpwncqszvftbrmjlhg: first marker after character 6
        nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 10
        zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 11
    """
    stream = input[0]
    packet_len = 4
    return find_packet_end(packet_len, stream)


def part_2(input, verbose=False):
    pass


def day_6(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
