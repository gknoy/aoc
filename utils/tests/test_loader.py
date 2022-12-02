"""
#
# test_loader.py: Test that we load advents
#
"""

from utils.loader import get_all_year_modules
from aoc_2021.days.day01 import day_1


def test_get_all_year_modules():
    all_modules = get_all_year_modules()
    assert all_modules[2021][0] == day_1
