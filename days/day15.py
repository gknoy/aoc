"""
# https://adventofcode.com/2021/day/15
"""
from typing import List, Tuple
from utils import get_line_items, Grid, Coord
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
# super-toy data while figuring out things
toy_data = [
    "1163", # "1163"
    "1381", # "1..."  => total risk is 11
    "2136", # "2136"
]


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


def build_grid_of_risks(input: List[str]) -> List[List[int]]:
    # n_rows = len(input)
    # n_cols = len(input[0])
    # grid = np.zeros([n_rows, n_cols], np.int8)
    grid = [[int(col) for col in row] for row in input]
    return grid


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

    def __iter__(self):
        return NodeIterator(self)

    def path_cost(self):
        return sum([node.cost for node in iter(self)])


def neighbors(node, grid: Grid):
    # TODO
    pass


def part_1(input, verbose=False):
    """
    Find total risk (cost/distance/etc) for the path with lowest risk

    You start in the top left position,
    your destination is the bottom right position, and
    you cannot move diagonally.

    [To] determine the total risk of an entire path, add up the risk levels of
    each position you enter (Start pos is never entered.)
    """
    grid = build_grid_of_risks(input)
    start = (0, 0)  # row, col
    goal = (len(grid) - 1, len(grid[0]) - 1)

    pass


def part_2(input, verbose=False):
    pass


def day_15(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
