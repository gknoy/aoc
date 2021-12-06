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


ADVENTS = {"1": day_1, "2": day_2, "3": day_3, "4": day_4, "5": day_5, "6": day_6}

# sanity check that I don't have a copy/paste error
assert len(set(ADVENTS.keys())) == len(set(ADVENTS.values())), "ADVENTS has a typo"


def _advent(item, use_toy_data, verbose):
    print(f"{item:>2}: {ADVENTS[item](use_toy_data=use_toy_data, verbose=verbose)}")


if __name__ == "__main__":
    use_toy_data = False
    verbose = False
    if "--toy" in sys.argv:
        use_toy_data = True
    if "--verbose" in sys.argv:
        verbose = True

    if "--all" in sys.argv:
        for item in ADVENTS.keys():
            _advent(item, use_toy_data, verbose)
    else:
        for item in sys.argv[1:]:
            if item in ["--toy", "--verbose"]:
                continue
            _advent(item, use_toy_data, verbose)
