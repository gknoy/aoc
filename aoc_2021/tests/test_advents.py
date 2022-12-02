#
# Sanity checks that all advents work even after refactoring
#
import pytest

from utils.loader import get_all_year_modules

ADVENTS = get_all_year_modules()
YEAR = 2021


class SkipTest:
    def __init__(self, reason, expected):
        self.reason = reason
        self.expected = expected


TOY_EXPECTED = {
    YEAR: {
        1: [7, 5],
        2: [150, 900],
        3: [198, 230],
        4: [4512, 1924],
        5: [5, 12],
        6: [5934, 26984457539],
        7: [37, 168],
        8: [26, 61229],
        9: [15, 1134],
        10: [26397, 288957],
        11: [1656, 195],
        12: [10, 36],
        13: [17, "CPZLPFZL"],  # fixme ;)
        14: [1588, 2188189693529],
        15: [40, 315],
    },
    2022: {},
}

EXPECTED = {
    YEAR: {
        1: [1298, 1248],
        2: [2147104, 2044620088],
        3: [4160394, 4125600],
        4: [39984, 8468],
        5: [4873, 19472],
        6: [396210, 1770823541496],
        7: [343468, 96086265],
        8: [255, 982158],
        9: [452, 1263735],
        10: [367059, 1952146692],
        11: [1691, 216],
        12: [4549, 120535],
        13: [607, "CPZLPFZL"],
        14: [3143, 4110215602456],
        15: [619, SkipTest("execution takes too long", 2922)],
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
