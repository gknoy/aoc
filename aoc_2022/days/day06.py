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
    return stream[index : index + n]


def is_unique_chars(chars, n_chars=4):
    return len(chars) == n_chars and len(set(chars)) == n_chars


def find_n_unique_chars(n_chars: int, stream: Sequence) -> int:
    for index in range(len(stream)):
        if is_unique_chars(window(index, n_chars, stream), n_chars):
            # print(f">>> index: {index} + {n_chars}")
            # print(stream[index: index + n_chars])
            return index + n_chars
    raise EOFError


def find_packet_start(stream):
    return find_n_unique_chars(4, stream)


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
    return find_packet_start(stream)


def part_2(input, verbose=False):
    """
    A start-of-message marker is just like a start-of-packet marker, except it consists of 14 distinct characters rather than 4.

    Here are the first positions of start-of-message markers for all of the above examples:

    mjqjpqmgbljsphdztnvjfqwrcgsmlb: first marker after character 19
    bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 23
    nppdvjthqldpwncqszvftbrmjlhg: first marker after character 23
    nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 29
    zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 26
    """
    stream = input[0]
    return find_message_start(stream)


def find_message_start(stream):
    """
    A start-of-message marker is just like a start-of-packet marker,
    except it consists of 14 distinct characters rather than 4.
    """
    return find_n_unique_chars(14, stream)


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


def day_6(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
