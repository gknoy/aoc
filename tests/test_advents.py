#
# Sanity checks that all advents work even after refactoring
#
import pytest
from advent import ADVENTS

TOY_EXPECTED = {
    1: [7, 5],
    2: [150, 900],
    3: [4160394, 4125600],
    4: [4512, 1924],
    5: [5, 12],
    6: [5934, 26984457539],
    7: [37, 168],
}

EXPECTED = {
    1: [1298, 1248],
    2: [2147104, 2044620088],
    3: [4160394, 4125600],
    4: [39984, 8468],
    5: [4873, 19472],
    6: [396210, 1770823541496],
    7: [343468, 96086265],
}


def _advent(item, use_toy_data=False, verbose=False):
    return ADVENTS[item](use_toy_data=use_toy_data, verbose=verbose)


@pytest.mark.parametrize(
    "key,expected", [(key, TOY_EXPECTED[int(key)]) for key in ADVENTS]
)
def test_toy_answers(key, expected):
    assert expected == _advent(key, use_toy_data=True)


@pytest.mark.parametrize("key,expected", [(key, EXPECTED[int(key)]) for key in ADVENTS])
def test_answers(key, expected):
    assert expected is not None
    assert expected == _advent(key, use_toy_data=False)
