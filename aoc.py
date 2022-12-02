#! /usr/bin/env python
"""
#
# advent.py
#
# Usage:
#   aoc.py 2021 1 --toy --verbose
#
"""
import sys

from utils.loader import get_all_year_modules, get_opts, get_advents_to_run

# {
#     2021: [day_1, day_2, ...],
#     2022: [day_1, day_2, ...],
# }
ADVENTS = get_all_year_modules()


def _advent(year, day, day_function, use_toy_data, verbose):
    print(
        f"{year} {day:>2}: {day_function(use_toy_data=use_toy_data, verbose=verbose)}"
    )


if __name__ == "__main__":
    options = get_opts(sys.argv[1:])
    advents_to_run = get_advents_to_run(ADVENTS, sys.argv[1:], options["--all"])
    for year, day, day_function in advents_to_run:
        _advent(year, day, day_function, options["--toy"], options["--verbose"])
