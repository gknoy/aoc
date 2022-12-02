"""
# https://adventofcode.com/2021/day/7
"""
import pytest
from statistics import mean, median

from utils import get_line_items, parse_one_line_input

input = list(get_line_items("input/07.txt"))
toy_input = ["16,1,2,0,4,2,7,1,2,14"]

# ---- Part 1: One fuel per move


def part_1(input, verbose=False):
    crabs = list(parse_one_line_input(input))

    def fuel_cost(distance):
        return int(abs(distance))

    def total_fuel_cost(pos, crabs):
        return sum(fuel_cost(crab - pos) for crab in crabs)

    median_crab_pos = int(median(crabs))
    return total_fuel_cost(median_crab_pos, crabs)


# ---- Part 2: cost increases by one each step


def exponential_fuel_cost(distance):
    return sum(range(abs(distance) + 1))


def pos_from_cost(desired_cost, cost_fn):
    cost = 0
    d = 0
    while cost < desired_cost:
        d += 1
        cost = cost_fn(d)
        print(f" cost({d}): {cost}")
        if cost == desired_cost:
            return d

    return d - 1


@pytest.mark.parametrize(
    "distance,expected",
    [
        [0, 0],
        # from toy example:
        [abs(16 - 5), 66],
        [abs(1 - 5), 10],
        [abs(2 - 5), 6],
        [abs(0 - 5), 15],
        [abs(4 - 5), 1],
        [abs(2 - 5), 6],
        [abs(7 - 5), 3],
        [abs(1 - 5), 10],
        [abs(2 - 5), 6],
        [abs(14 - 5), 45],
    ],
)
def test_exponential_fuel_cost(distance, expected):
    assert expected == exponential_fuel_cost(distance)


def part_2(input, verbose=False):
    crabs = list(parse_one_line_input(input))

    def all_crab_fuel_costs(pos, crabs):
        return [exponential_fuel_cost(crab - pos) for crab in crabs]

    def brute_force_min_fuel_costs(crabs, min_pos, max_pos):
        """
        The ugly solution is to call this on the full range of crabs,
        so that we are effectively (in the worst case) doing 1000 * N
        cost calculations.

        :param crabs: An array of crab positions
        :param min_pos: the leftmost position to try
        :param max_pos: the rightmost position to try
        :return: cheapest total cost
        """
        # This can almost certainly be done better than O(N^2),
        # but I haven't figured out how.
        min_cost = None
        for pos in range(min_pos, max_pos):
            crab_costs = all_crab_fuel_costs(pos, crabs)
            cost = sum(crab_costs)
            # if verbose:
            #     print(f" pos: {pos}  cost: {cost}")  # "  crab_costs: {crab_costs}")
            if min_cost is None or cost < min_cost:
                min_cost = cost
            # if verbose:
            if cost > min_cost:
                if verbose:
                    print(f" pos: {pos-1}  cost: {min_cost}")
                return min_cost
        return min_cost

    # --------------------
    # Range Optimizations
    # --------------------
    # We obviously don't want to call brute_force_min_fuel_costs with ALL
    # of the possible positions, as that's 1000*1000 loops for our data.
    # However, if we can throw out the most extreme of the movement targets,
    # that means we don't have to

    # If we look at the costs for things to move the FARTHEST,
    # such as to the smallest or to the largest crab positions, we notice
    # that looking at the mean costs suggests some bounds:
    #
    #     crabs: [0, 1, 1, 2, 2, 2,  4 , 7,  14, 16]
    #   to zero: [0, 1, 1, 3, 3, 3, 10, 28, 105, 136]
    #      mean: 29                        ^
    #
    #        => I think this tells us nothing useful, except
    #           perhaps that the solution is to the left of 14 (?)
    #
    #     crabs: [  0,   1,   1,   2,   2,   2,  4,  7, 14, 16]
    #    to max: [136, 120, 120, 105, 105, 105, 78, 45,  3,  0]
    #      mean: 81.7                          ^
    #
    #        => I think this tells us nothing useful, except
    #           perhaps that the solution is to the right of 2 (?).
    #
    #     crabs: [  0,   1,   1,   2,   2,   2,  4,  7,  14,  16]
    #      both: [136, 121, 121, 108, 108, 108, 88, 73, 108, 136]  mean: 110.7
    #                                            ^   ^     ^
    #                                     last asc   |     first ascending
    #                                   before min   |
    #                                                min in set
    #
    #                            ^^^^^^^^^^^^^^^^^^^^^^^^^^ smaller than mean
    #                                         >>>       <<<
    #        => Interestingly, the range bounds suggested by looking at
    #           the mean of the sum of extreme movement costs seems to be
    #           larger in both directions. I've not thought about this enough
    #           to be sure whether it's always true or not.
    #

    # We need these pre-sorted so that we can squeeze the side bounds
    sorted_crabs = sorted(crabs)

    costs_to_left = all_crab_fuel_costs(sorted_crabs[0], sorted_crabs)
    costs_to_right = all_crab_fuel_costs(sorted_crabs[-1], sorted_crabs)
    # e.g.: [105, 92, 92, 81, 81, 81, 65, 56, 105, 136]
    sum_of_both_extremes = [a + b for a, b in zip(costs_to_left, costs_to_right)]
    mean_cost_to_zero = mean(costs_to_left)
    mean_cost_to_max = mean(costs_to_right)
    mean_cost_extreme = mean(sum_of_both_extremes)
    if verbose:
        print(f">>> mean_cost_extreme: {mean_cost_extreme}")

    range_from_lt = lambda: range(0, len(crabs), 1)
    range_from_rt = lambda: range(len(crabs) - 1, 0, -1)

    def squeeze_bounds(costs, mean_cost, range_indexes):
        min_pos = sorted_crabs[0]
        for index in range_indexes:
            if costs[index] > mean_cost:
                min_pos = sorted_crabs[index]
            else:
                break
        return min_pos

    min_pos = sorted_crabs[0]
    max_pos = sorted_crabs[-1]
    if verbose:
        print(f">>> min pos: {min_pos}  max pos: {max_pos}")

    max_pos_from_leftward_costs = squeeze_bounds(
        costs_to_left, mean_cost_to_zero, range_from_rt()
    )
    min_pos_from_rightward_costs = squeeze_bounds(
        costs_to_right, mean_cost_to_max, range_from_lt()
    )

    min_x_from_extreme = squeeze_bounds(
        sum_of_both_extremes, mean_cost_extreme, range_from_lt()
    )
    max_pos_from_extreme = squeeze_bounds(
        sum_of_both_extremes, mean_cost_extreme, range_from_rt()
    )

    max_pos = min(max_pos_from_leftward_costs, max_pos_from_extreme)
    min_pos = max(min_pos_from_rightward_costs, min_pos_from_rightward_costs)

    if verbose:
        print(f">>> min pos: {min_pos_from_rightward_costs}  (based on >>> cost)")
        print(f">>> max pos: {max_pos_from_leftward_costs}  (based on <<< cost)")
        print(f">>> min pos: {min_x_from_extreme}  (based on l+r total)")
        print(f">>> max pos: {max_pos_from_extreme}  (based on l+r total)")
        print(f">>> min pos: {min_pos}  max pos: {max_pos}")
        print(f">>> min pos: {min_pos}  max pos: {max_pos}")

    def _debug(desc, items):
        if verbose:
            print(f" -- {desc}: mean: {mean(items)}")

    # print(f" -- crabs: {sorted_crabs}")
    _debug(" zero", costs_to_left)
    _debug("  max", costs_to_right)
    _debug(" both", sum_of_both_extremes)

    return brute_force_min_fuel_costs(crabs, min_pos, max_pos)


def day_7(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
