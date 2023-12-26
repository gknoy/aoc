"""
# https://adventofcode.com/2023/day/5
"""
from dataclasses import dataclass
from functools import cached_property
from utils.utils import get_line_items

input = list(get_line_items("aoc_2023/input/05.txt"))
toy_input: list[str] = [
    # fmt: off
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
    "",
    "fertilizer-to-water map:",
    "49 53 8",
    "0 11 42",
    "42 0 7",
    "57 7 4",
    "",
    "water-to-light map:",
    "88 18 7",
    "18 25 70",
    "",
    "light-to-temperature map:",
    "45 77 23",
    "81 45 19",
    "68 64 13",
    "",
    "temperature-to-humidity map:",
    "0 69 1",
    "1 0 69",
    "",
    "humidity-to-location map:",
    "60 56 37",
    "56 93 4",
    # fmt: on
]


# ------------------
# Part 1
# ------------------
# Every type of seed, soil, fertilizer and so on is identified with a number
# Numbers are reused by each category
# soil 123 and fertilizer 123 aren't necessarily related
#
# NOTE: A plain dict is probably not sufficient, as valaue ranges are _really big_:
#
#   seed-to-soil map:
#   357888202 777841571 45089383
#   1091769591 2222785614 212172358
#   747211456 668867483 108974088
#   # ....


@dataclass
class MapSegment:
    """
    (dest range start, source range start, range count)

    intended usage:
    for segment in segment:
        if input in segment:
            return segment[input]
    return input
    """

    dest_start: int
    source_start: int
    size: int

    @cached_property
    def dest_end(self):
        return self.dest_start + self.size

    @cached_property
    def source_end(self):
        return self.source_start + self.size

    def __contains__(self, source_index):
        return self.source_start <= source_index < self.source_end

    def __len__(self):
        return self.size

    def __lt__(self, other):
        # The sort algorithm uses only < comparisons between items
        # We only care about source mapping indexes so that we can
        return self.source_start < other.source_start

    def __getitem__(self, index):
        """Used when checking whether input is in range that we handle"""
        if index < self.source_start or index >= self.source_end:
            raise IndexError(
                f"Segment intput range ({self.source_start}, {self.source_start}) "
                f"does not contain [{index}]"
            )
        delta = index - self.source_start
        assert delta <= self.size, "delta > range_count"
        return self.dest_start + delta


class Mapping:
    """
    Take a list of mapping segments
      (dest range start, source range start, range count)
    50 98 2
    52 50 48
    """

    def __init__(self, mappings):
        self.map_segments = list(sorted(mappings))

    def __getitem__(self, index):
        # get the "destination index" when we query an input index
        for mapping in self.map_segments:
            print(f">>> segment: {(mapping.source_start, mapping.source_end)}")
            if index in mapping:
                return mapping[index]
        # If we don't have a custom mapping for this index,
        # then it maps to the same destination
        print(f"un-mapped index {index}")
        return index


def parse_segment(line):
    dest_start, source_start, size = [int(item) for item in line.split()]
    return MapSegment(dest_start=dest_start, source_start=source_start, size=size)


def part_1(input, verbose=False):
    pass


# ------------------
# Part 2
# ------------------


def part_2(input, verbose=False):
    pass


def day_5(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
