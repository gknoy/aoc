#
# Sanity checks that all advents work even after refactoring
#
import pytest

from utils.loader import get_all_year_modules

ADVENTS = get_all_year_modules()
YEAR = 2022


class SkipTest:
    def __init__(self, reason, expected):
        self.reason = reason
        self.expected = expected


# Disable black formatting of expected values, because
# with short enough numbers of items it's less convenient to add a new day. :)
# fmt: off
TOY_EXPECTED = {
    YEAR: {
        1: [24000, 45000],
        2: [15, 12],
        3: [157, 70],
        4: [2, 4],
        5: ["CMZ", "MCD"],
        6: [7, None],
    },
}

EXPECTED = {
    YEAR: {
        1: [70296, 205381],
        2: [10404, 10334],
        3: [7831, 2683],
        4: [556, 876],
        5: ["QPJPLMNNR", "BQDNWJPVJ"],
        6: [1816, None],
    }
}
# fmt: on


def _advent(day_index, use_toy_data=False, verbose=False):
    return ADVENTS[YEAR][day_index - 1](use_toy_data=use_toy_data, verbose=verbose)


@pytest.mark.parametrize(
    "key,expected",
    [
        (day_number, TOY_EXPECTED[YEAR][day_number])
        for day_number in range(1, 1 + len(ADVENTS[YEAR]))
    ],
)
def test_toy_answers(key, expected):
    assert expected == _advent(key, use_toy_data=True)


@pytest.mark.parametrize(
    "key,expected",
    [
        (day_number, EXPECTED[YEAR][day_number])
        for day_number in range(1, 1 + len(ADVENTS[YEAR]))
    ],
)
def test_answers(key, expected):
    assert expected is not None
    if type(expected) is not SkipTest:
        assert expected == _advent(key, use_toy_data=False)
    else:
        assert True
