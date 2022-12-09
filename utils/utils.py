# ----------------------
# advent infrastructure
# ----------------------
from typing import Any, Generator, List, Set, Tuple

BOLD = "\033[1m"
CLEAR = "\033[0m"


# custom type
Coord = Tuple[int, int]
Grid = List[List[int]]


def get_line_items(fname) -> Generator[str, Any, None]:
    """Read all the lines from an input file into an array of strings"""
    with open(fname) as f:
        # 2022, day 5: rstrip vs strip: don't strip leading whitespace!
        return (item.rstrip() for item in f.readlines())


def parse_one_line_input(input: List[str]) -> List[int]:
    line = input[0]
    return list(map(int, line.split(",")))


def digits_array(digits_str: str) -> List[int]:
    """
    Split a string of digits into a list of ints
    "010" -> [0, 1, 0]
    """
    return list(map(int, digits_str))


def two_d_array_from_digit_strings(data: List[str]) -> Grid:
    """
    :param data: A list of strings of digits
    :return: A list of lists of digits
    """
    # ["010", "001"] -> [[0,1,0], [0,0,1]]
    # return np.array(digits_array(number_str) for number_str in data)
    return list(digits_array(number_str) for number_str in data)


def vertical_slice(data: List[List[Any]], index: int) -> List[Any]:
    return [item[index] for item in data]


def digits_to_int(digits: List[int], base=10) -> int:
    digit_strings = [str(digit) for digit in digits]
    return int("".join(digit_strings), base)


def up(coord: Coord, min_row=0) -> Coord:
    return (max(min_row, coord[0] - 1), coord[1])


def down(coord: Coord, max_row) -> Coord:
    return (min(max_row, coord[0] + 1), coord[1])


def left(coord: Coord, min_col=0) -> Coord:
    return (coord[0], max(min_col, coord[1] - 1))


def right(coord: Coord, max_col) -> Coord:
    return (coord[0], min(max_col, coord[1] + 1))


def neighbors(coord: Coord, max_row, max_col, include_diagonals=True) -> Set[Coord]:
    diagonal_neighbors = (
        {
            left(up(coord)),
            left(down(coord, max_row)),
            right(up(coord), max_col),
            right(down(coord, max_row), max_col),
        }
        if include_diagonals
        else {}
    )
    return {
        *diagonal_neighbors,
        up(coord),
        down(coord, max_row),
        left(coord),
        right(coord, max_col),
    } ^ {coord}
