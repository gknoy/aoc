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


TOY_EXPECTED = {
    YEAR: {
        1: [24000, 45000],
    },
}

EXPECTED = {
    YEAR: {
        1: [70296, 205381],
    }
}


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
