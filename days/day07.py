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
    return sum(range(abs(distance + 1)))


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
    print(f">>> {len(crabs)} crabs")

    # FIXME REMOVE once I don't have an O(n^2) soln
    crabs = crabs[:20]

    def total_fuel_cost(pos, crabs):
        return sum(exponential_fuel_cost(abs(crab - pos)) for crab in crabs)

    def all_crab_fuel_costs(pos, crabs):
        return [exponential_fuel_cost(abs(crab - pos)) for crab in crabs]

    def brute_force_min_fuel_costs(crabs):
        # This can almost certainly be done better than O(N^2),
        # and I'm working on a less ugly solution.
        min_cost = None
        print(f"crabs: {crabs}")
        for pos in range(0, crabs[-1]):
            crab_costs = all_crab_fuel_costs(pos, crabs)
            cost = sum(crab_costs)
            print(f" pos: {pos}  cost: {cost}  crab_costs: {crab_costs}")
            if min_cost is None or cost < min_cost:
                min_cost = cost
            if cost > min_cost:
                return min_cost
        return min_cost

    # FIXME: No. Don't do this.
    return brute_force_min_fuel_costs(crabs)


def day_7(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
