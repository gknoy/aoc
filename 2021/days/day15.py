"""
# https://adventofcode.com/2021/day/15
"""
from math import inf
from typing import Dict, List
from collections import Counter
from utils import get_line_items, Grid, Coord, neighbors, two_d_array_from_digit_strings

# import numpy as np
# from numpy.typing import ArrayLike, NDArray


input = list(get_line_items("input/15.txt"))
toy_input: List[str] = [
    "1163751742",
    "1381373672",
    "2136511328",
    "3694931569",
    "7463417111",
    "1319128137",
    "1359912421",
    "3125421639",
    "1293138521",
    "2311944581",
]
# # # super-toy data while figuring out things
# toy_input = [
#     "1163", # "1..."
#     "1381", # "1..."  => total risk is 13 (ignore start pos)
#     "2136", # "2136"
# ]


# --------------------
# Part 1: A* search
#
#   Lowest total risk effectively similar as the shortest path to the goal,
#   where the risk at each coordinate can be considered the cost to enter
#   that node from a neighbor.
#   This is better than Dijkstra's because we have a single goal node.
#
#   https://en.wikipedia.org/wiki/A*_search_algorithm
#
#   Maintain a set of candidate nodes that we've visited.
#   - Pick the one(s) with the lowest f(n) = g(n) + h(n)
#       g(n): distance/cost so far
#       h(n): heuristic of cost to goal (e.g. manhattan distance for grid)
#   - A* terminates when the path it chooses to extend is a path from start to goal
#     or if there are no paths eligible to be extended.
# --------------------


class NodeIterator:
    # TIL not to make the iterator the same as the node class ;)
    def __init__(self, node):
        self.node = node

    def __iter__(self):
        return self

    def __next__(self):
        if self.node is None:
            raise StopIteration
        current = self.node
        self.node = self.node.prev
        return current


class Node:
    def __init__(self, coords: Coord, cost: int, prev=None):
        self.coords = coords
        self.prev = prev
        # cost to enter this node (not total cost)
        self.cost = 0 if prev is None else cost
        self.path_cost = self.cost
        if prev is not None:
            self.path_cost += prev.path_cost

    # def __hash__(self):
    #     return hash(self.coords)
    #
    # def __eq__(self, other):
    #     return self.coords == other.coords

    def __iter__(self):
        return NodeIterator(self)

    def __repr__(self):
        return f"<{self.coords}: {self.path_cost}>"


def a_star(start: Coord, goal: Coord, grid: Grid, verbose=False, max_iter=60000) -> Node:
    #   Maintain a set of candidate nodes that we've visited.
    #   - Pick the one(s) with the lowest f(n) = g(n) + h(n)
    #       g(n): distance/cost so far
    #       h(n): heuristic of cost to goal (e.g. manhattan distance for grid)
    #   - A* terminates when the path it chooses to extend is a path from start to goal
    #     or if there are no paths eligible to be extended.
    start_node = Node(coords=start, cost=0, prev=None)
    max_row = len(grid) - 1
    max_col = len(grid[0]) - 1

    def _grid(coords):
        row, col = coords
        return grid[row][col]

    def g(node):
        return node.path_cost

    def h(node):
        # manhattan distance
        # this guarantees best cost since it'll be <= the real cost
        return (goal[0] - node.coords[0]) + (goal[1] - node.coords[1])

    def f(node):
        return g(node) + h(node)

    def pick(candidates: Dict[Coord, Node]):
        # FIXME: We often have ~1000 candidates.
        #   This means that sorting is stupid, all I need to track is the
        #   minimum cost + node
        best_f = inf
        best = None
        fn, fn, hn = (inf, inf, inf)
        for coords, node in candidates.items():
            fn = f(node)
            gn = g(node)
            hn = h(node)
            if fn < best_f:
                best_f = fn
                best = node
        return best, fn, gn, hn

    # we'd normally store these in a set, but i want to be able to see
    # the previous cheapest path to a node and compare vs a new one
    candidates = {start: start_node}
    visited = set()
    current = start_node  # we know it's the only one to pick, initially
    iteration = 0
    while candidates:
        if iteration > max_iter:
            raise StopIteration
        current, fn, gn, hn = pick(candidates)
        visited.add(current.coords)
        if verbose:
            print(
                f">>> iteration {iteration:>5} "
                f"candidates: {len(candidates)} "
                f"visited {len(visited)} best: {current.path_cost}"
                f" f(n): {fn} g(n): {gn} h(n): {hn}"
            )
        if current.coords == goal:
            # we know it has the lowest cost, since we picked it, so it's
            # our shortest path to goal.
            return current

        del candidates[current.coords]
        for coords in neighbors(
            current.coords, max_row, max_col, include_diagonals=False
        ):
            new_node = Node(coords, _grid(coords), current)
            if coords not in visited:
                # if we get to a node in a different way, make sure that
                # this is cheaper to get there than the earlier way we got there.
                if coords in candidates:
                    existing_candidate = candidates[coords]
                    if new_node.path_cost >= existing_candidate.path_cost:
                        continue
                candidates[coords] = new_node
        iteration += 1

    # if there are no more candidates, then we are done.
    return current


def part_1(input, verbose=False):
    """
    Find total risk (cost/distance/etc) for the path with lowest risk

    You start in the top left position,
    your destination is the bottom right position, and
    you cannot move diagonally.

    [To] determine the total risk of an entire path, add up the risk levels of
    each position you enter (Start pos is never entered.)
    """
    grid = two_d_array_from_digit_strings(input)
    start = (0, 0)  # row, col
    goal = (len(grid) - 1, len(grid[0]) - 1)

    path_node = a_star(start, goal, grid, verbose=verbose)
    if verbose:
        print(f">>> goal: {goal}")
        print(f">>> path: {[node for node in reversed(list(path_node))]}")
    return path_node.path_cost


def create_tiled_map(grid, n_tiles = 5):
    # oh heck we should use numpy now ...
    # FIXME
    def rollover(n):
        return n if n <= 9 else n - 9

    def _tile(row, delta):
        return [
            rollover(item + delta) for item in row
        ]

    new_grid = []
    for tile_row_index in range(n_tiles):
        for row in grid:
            extended_row = []
            for tile_col_index in range(n_tiles):
                extended_row += _tile(row, tile_col_index + tile_row_index)
            new_grid.append(extended_row)

    return new_grid


def test_create_tiled_map():
    orig = [[8]]
    tiled = create_tiled_map(orig, 5)
    assert tiled == [
        [8, 9, 1, 2, 3,],
        [9, 1, 2, 3, 4,],
        [1, 2, 3, 4, 5,],
        [2, 3, 4, 5, 6,],
        [3, 4, 5, 6, 7,],
    ]


def part_2(input, verbose=False):
    """
    Grid is actually 5x5 tiled from input

    Your original map tile repeats to the right and downward;
    each time the tile repeats to the right or downward, all of its risk levels
    are 1 higher than the tile immediately up or left of it
    Risk levels above 9 wrap back around to 1

    >>> iteration 249985 candidates: 9 visited 249986 best: 2922 f(n): 2930 g(n): 2924 h(n): 6
    >>> goal: (499, 499)
    """

    original_grid = two_d_array_from_digit_strings(input)
    grid = create_tiled_map(original_grid)
    start = (0, 0)  # row, col
    goal = (len(grid) - 1, len(grid[0]) - 1)

    path_node = a_star(start, goal, grid, verbose=verbose, max_iter=250000)
    if verbose:
        print(f">>> goal: {goal}")
        print(f">>> path: {[node for node in reversed(list(path_node))]}")
    return path_node.path_cost


def day_15(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
