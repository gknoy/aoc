#! /usr/bin/env python
"""
#
# advent.py
#
"""
import sys

from days.day01 import day_1
from days.day02 import day_2
from days.day03 import day_3
from days.day04 import day_4
from days.day05 import day_5
from days.day06 import day_6
from days.day07 import day_7
from days.day08 import day_8
from days.day09 import day_9
from days.day10 import day_10
from days.day11 import day_11
from days.day12 import day_12

# Harvest from globals() so that I don't need to add both an import
# AND a key/value pair each day
ADVENTS = {
    k.replace("day_", ""): v for k, v in globals().items() if k.startswith("day_")
}

# sanity check that I don't have a copy/paste error
assert len(set(ADVENTS.keys())) == len(set(ADVENTS.values())), "ADVENTS has a typo"


def _advent(item, use_toy_data, verbose):
    print(f"{item:>2}: {ADVENTS[item](use_toy_data=use_toy_data, verbose=verbose)}")


if __name__ == "__main__":
    use_toy_data = False
    verbose = False

    options = [item for item in sys.argv[1:] if item.startswith("--")]
    use_all = "--all" in options
    advents_to_run = [
        item for item in ADVENTS.keys() if use_all or item in sys.argv
    ] or ADVENTS.keys()

    if "--toy" in sys.argv:
        use_toy_data = True
    if "--verbose" in sys.argv:
        verbose = True

    for item in advents_to_run:
        _advent(item, use_toy_data, verbose)
