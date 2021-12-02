"""
#
# advent.py
#
"""
import sys

# ----------------------
# advent infrastructure
# ----------------------


def get_line_items(fname):
    with open(fname) as f:
        return (item.strip() for item in f.readlines())


# ----------------------
# advent problems
# ----------------------


def one():
    """
    Count how many times measurement is larger than previous measurement
    https://adventofcode.com/2021/day/1
    """
    measurements = [int(item) for item in get_line_items("input/1.txt")]

    def count_increasing_measurements(measurements):
        return sum(
            [
                1
                for index, item in enumerate(measurements)
                if (index > 0 and measurements[index] > measurements[index - 1])
            ]
        )

    return count_increasing_measurements(measurements)


# -----------------------
# actually run things ...
# -----------------------

ADVENTS = {
    "1": one,
}


if __name__ == "__main__":
    for item in sys.argv[1:]:
        print(f"--- {item} ---")
        # TODO benchmarks
        print(ADVENTS[item]())
