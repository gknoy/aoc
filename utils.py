# ----------------------
# advent infrastructure
# ----------------------
from typing import Any, Generator, List

BOLD = "\033[1m"
CLEAR = "\033[0m"


def get_line_items(fname) -> Generator[str]:
    """Read all the lines from an input file into an array of strings"""
    with open(fname) as f:
        return (item.strip() for item in f.readlines())


def parse_one_line_input(input: List[str]) -> List[int]:
    line = input[0]
    return list(map(int, line.split(",")))


def digits_array(digits_str: str) -> List[int]:
    """
    Split a string of digits into a list of ints
    "010" -> [0, 1, 0]
    """
    return list(map(int, digits_str))


def two_d_array_from_digt_strings(data: List[str]) -> List[List[int]]:
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
