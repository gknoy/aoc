"""
# https://adventofcode.com/2023/day/3
"""
import functools
import itertools
from dataclasses import dataclass

from utils.utils import get_line_items

input = list(get_line_items("aoc_2023/input/03.txt"))
toy_input: list[str] = [
    # fmt: off
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
    # fmt: on
]

# -----------------------------
# Part 1
# -----------------------------
# Symbol: any character that isn't a digit and isn't a '.'
# Any number adjacent to a symbol, even diagonally, is a "part number"


@dataclass
class Item:
    start: int = 0
    end: int = 0

    def __hash__(self):
        return hash((self.start, self.end))

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __lt__(self, other):
        return self.start < other.start and self.end < other.end

    def __gt__(self, other):
        return self.start > other.start and self.end > other.end


@dataclass
class Symbol(Item):
    name: str = None

    def __hash__(self):
        return hash(("S", self.start, self.end, self.name))


@dataclass
class PartNumber(Item):
    value: int | str = None

    def __hash__(self):
        return hash(("PN", self.start, self.end, self.value))


GridRow = list[Symbol | PartNumber]
Grid = list[GridRow]
Position = tuple[int, int]  # row, col


@functools.cache
def is_digit(c: str) -> bool:
    return c in "0123456789"


@functools.cache
def is_symbol(c: str) -> bool:
    return c != "." and not is_digit(c)


def parse_line(line: str) -> GridRow:
    # the current-parsing-thing (We can just directly store symbols)
    current: PartNumber | None = None
    found = []

    for index in range(len(line)):
        c = line[index]

        if is_digit(c):
            if current is None:
                # first digit of new number
                current = PartNumber(
                    start=index,
                    end=index + 1,  # changed once we find end of string
                    value=int(c),
                )
                continue
            if type(current) is PartNumber:
                #
                current.value = int(f"{current.value}{c}")
                current.end = index + 1
                continue
        if c == ".":
            if current is None:
                continue
            if type(current) is PartNumber:
                # store it because we're done
                found.append(current)
                current = None
        if is_symbol(c):
            # save current if needed
            if type(current) is PartNumber:
                # store it because we've found something else
                found.append(current)
            # save this symbol too
            found.append(Symbol(name=c, start=index, end=index + 1))
            current = None
    return found


def get_adjacent_positions(pos: Position) -> list[Position]:
    r, c = pos
    offsets = [-1, 0, 1]

    return [
        (r + row_offset, c + col_offset)
        for row_offset in offsets
        for col_offset in offsets
        # exclude original position ;)
        if (r + row_offset, c + col_offset) != (r, c)
    ]


def get_at_position(grid: Grid, pos: tuple[int, int]) -> Item | None:
    row, col = pos
    if row < 0 or row >= len(grid):
        return None
    # we don't care about row bounds because items store their locations
    for item in grid[row]:
        if item.start <= col < item.end:
            return item
    return None


def get_adjacent_parts(grid: Grid, pos) -> list[PartNumber]:
    adj_positions = get_adjacent_positions(pos)
    candidates = set([get_at_position(grid, adj_pos) for adj_pos in adj_positions])
    return [item for item in candidates if item is not None and type(item) is PartNumber]


def find_part_numbers(grid: Grid) -> list[PartNumber]:
    """
    Get all part numbers that are adjacent to a symbol
    Assume some parts can be adjacent to multiple symbols
    """
    for row_index in range(len(grid)):
        for item in grid[row_index]:
            if type(item) is Symbol:
                for part in get_adjacent_parts(grid, (row_index, item.start)):
                    yield part


def parse_grid(lines: list[str]) -> Grid:
    return [parse_line(line) for line in lines]


def part_1(input, verbose=False):
    grid = parse_grid(input)
    part_numbers = list(find_part_numbers(grid))
    numbers = [part.value for part in part_numbers]
    return sum(numbers)


def part_2(input, verbose=False):
    pass


def day_3(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
