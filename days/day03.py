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


def calc_gamma_digits(digits):
    """
    Most common bit in each column of digits
    ties go to 1
    """
    # GAMMA:
    #   Each bit in the gamma rate is the most common bit in the corresponding
    #   position of all numbers in the diagnostic report.
    item_len = len(digits[0])
    one_counts = [sum(vertical_slice(digits, index)) for index in range(item_len)]
    return [(1 if item >= (len(digits) / 2) else 0) for item in one_counts]


def invert_bits(gamma_digits):
    # invert bits
    xform = [1, 0]
    return [xform[d] for d in gamma_digits]


def part_1(data):
    # power consumption
    digits = data_digits(data)

    gamma_digits = calc_gamma_digits(digits)
    epsilon_digits = invert_bits(gamma_digits)

    gamma = digits_to_int(gamma_digits)
    epsilon = digits_to_int(epsilon_digits)

    def power_consumption(gamma, epsilon):
        return gamma * epsilon

    return power_consumption(gamma, epsilon)


def filter_data_by_column_value_freq(data, col, most_frequent=True):
    if len(data) == 1:
        return data
    most_common_bits = calc_gamma_digits(data)
    least_common_bits = invert_bits(most_common_bits)

    freq = most_common_bits if most_frequent else least_common_bits
    return [item for item in data if item[col] == freq[col]]


def part_2(data):
    # life support rating
    digits = data_digits(data)

    item_len = len(digits[0])

    oxy_vals = digits
    for col_index in range(item_len):
        oxy_vals = filter_data_by_column_value_freq(oxy_vals, col_index, True)

    co2_vals = digits
    for col_index in range(item_len):
        co2_vals = filter_data_by_column_value_freq(co2_vals, col_index, False)

    oxy_rating = digits_to_int(oxy_vals[0])
    scrubber_rating = digits_to_int(co2_vals[0])

    return oxy_rating * scrubber_rating


def day_3(use_toy_data=False):
    _data = toy_data if use_toy_data else data
    return [part_1(_data), part_2(_data)]
