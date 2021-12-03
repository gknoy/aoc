"""
# Day 3: Binary Diagnostic
#
# https://adventofcode.com/2021/day/3
"""
from utils import get_line_items

toy_data = [
    "00100",
    "11110",
    "10110",
    "10111",
    "10101",
    "01111",
    "00111",
    "11100",
    "10000",
    "11001",
    "00010",
    "01010",
]

data = [item for item in get_line_items("input/03.txt")]


def digits_array(digits_str):
    # "010" -> [0, 1, 0]
    return list(map(int, digits_str))


def data_digits(data):
    # ["010", "001"] -> [[0,1,0], [0,0,1]]
    # return np.array(digits_array(number_str) for number_str in data)
    return list(digits_array(number_str) for number_str in data)


def vertical_slice(data, index):
    return [item[index] for item in data]


def digits_to_int(digits):
    digit_strings = [str(digit) for digit in digits]
    return int("".join(digit_strings), 2)


def part_1(data):
    item_len = len(data[0])  # each datum is the same length
    digits = data_digits(data)

    one_counts = [sum(vertical_slice(digits, index)) for index in range(item_len)]

    # GAMMA:
    #   Each bit in the gamma rate ... the most common bit in the corresponding
    #   position of all numbers in the diagnostic report.
    gamma_digits = [(1 if item >= (len(data) / 2) else 0) for item in one_counts]

    def epsilon_from(gamma_digits):
        # invert bits
        xform = [1, 0]
        return [xform[d] for d in gamma_digits]

    epsilon_digits = epsilon_from(gamma_digits)

    gamma = digits_to_int(gamma_digits)
    epsilon = digits_to_int(epsilon_digits)

    def power_consumption(gamma, epsilon):
        return gamma * epsilon

    return power_consumption(gamma, epsilon)


def part_2(data):
    return None


def day_3(use_toy_data=False):
    _data = toy_data if use_toy_data else data
    return [part_1(_data), part_2(_data)]
