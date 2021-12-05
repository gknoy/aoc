#
# Sanity checks that all advents work even after refactoring
#
from advent import ADVENTS

TOY_EXPECTED = {
    1: [7, 5],
    2: [150, 900],
    3: [4160394, 4125600],
    4: [4512, 1924],
    5: [5, 12],
}

EXPECTED = {
    1: [1298, 1248],
    2: [2147104, 2044620088],
    3: [4160394, 4125600],
    4: [39984, 8468],
    5: [4873, 19472],
}


def _advent(item, use_toy_data=False, verbose=False):
    return ADVENTS[item](use_toy_data=use_toy_data, verbose=verbose)


def test_advents():
    for key in ADVENTS:
        e_key = int(key)
        assert TOY_EXPECTED[e_key] == _advent(key, use_toy_data=True)
        assert EXPECTED[e_key] == _advent(key, use_toy_data=False)
