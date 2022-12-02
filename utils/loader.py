"""
#
# loader.py
#
# A nicer way to load _all the days_ for a given year, so that we don't
# need to do weird crap with cut/paste and
#
"""
import importlib
import os
import re

from collections import defaultdict
from typing import Dict, List, Tuple, Callable
from types import ModuleType


DAY_PATTERN = re.compile(r"^day\d+.py$")
YEAR_PATTERN = re.compile(r"^aoc_(\d+)$")
DAY_FUNCTION_PATTERN = re.compile(r"^day(_\d+)?$")  # "day" or "day_N"


def get_year_dirs() -> List[Tuple[str, str]]:
    items = []
    for dirname in sorted(os.listdir("./")):
        m = YEAR_PATTERN.match(dirname)
        if m is None:
            continue
        # m.group() yields the whole string.
        items.append((dirname, m.group(1)))
    return items


def get_day_names(year_dir) -> List[str]:
    return [
        fname  # e.g. "day01.py"
        for fname in sorted(os.listdir(f"./{year_dir}/days/"))
        if DAY_PATTERN.match(fname)
    ]


def get_day_module(day_fname, year_dir) -> ModuleType:
    # e.g "aoc_2021.days.day01"
    day_path = ".".join([year_dir, "days", day_fname[:-3]])
    return importlib.import_module(day_path)


def get_day_function(day_module: ModuleType):
    """find the day() or day_\\d+"""
    keys = [k for k in day_module.__dict__ if DAY_FUNCTION_PATTERN.match(k)]
    assert 1 == len(keys)
    day_func: Callable = getattr(day_module, keys[0])
    return day_func


def get_all_year_modules() -> Dict[int, List[Callable]]:
    return {
        int(year): [
            get_day_function(get_day_module(fname, year_dir))
            for fname in get_day_names(year_dir)
        ]
        for year_dir, year in get_year_dirs()
    }


# ------------------
# invocation helpers
# ------------------


def get_int_args(argv):
    args = []
    for arg in argv:
        try:
            args.append(int(arg))
        except:
            pass
    return args


def get_opts(argv: List[str]) -> Dict[str, bool]:
    options = [item for item in argv if item.startswith("--")]
    return defaultdict(bool, {opt: True for opt in options})


def get_advents_to_run(advents, argv, use_all=False):
    year, *days = get_int_args(argv)
    # import ipdb; ipdb.set_trace()###REMOVE
    if use_all:
        return [
            # fmt: off
            (year, index + 1, day)
            for year in sorted(advents.keys())
            for index, day in enumerate(advents[year])
            # fmt: on
        ]
    if len(days) == 0:
        days = range(1, len(advents[year]) + 1)
    return [
        # input is 1-indexed ;)
        (year, day, advents[year][day - 1])
        for day in days
    ]
