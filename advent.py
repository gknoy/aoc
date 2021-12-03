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


ADVENTS = {"1": day_1, "2": day_2, "3": day_3}

# sanity check that I don't have a copy/paste error
assert len(set(ADVENTS.keys())) == len(set(ADVENTS.values())), "ADVENTS has a typo"


def _advent(item):
    print(f"{item:>2}: {ADVENTS[item](use_toy_data=use_toy_data)}")


if __name__ == "__main__":
    use_toy_data = False
    if "--toy" in sys.argv:
        use_toy_data = True

    if "--all" in sys.argv:
        for item in ADVENTS.keys():
            _advent(item)
    else:
        for item in sys.argv[1:]:
            if item == "--toy":
                continue
            _advent(item)
