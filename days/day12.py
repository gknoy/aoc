"""
# Passage Pathing
# https://adventofcode.com/2021/day/12
"""
from functools import cached_property
from typing import Dict, List
from utils import get_line_items

input = list(get_line_items("input/12.txt"))
toy_input: List[str] = [
    # # 10 paths:
    # #      start
    # #      /   \
    # #  c--A-----b--d
    # #      \   /
    # #       end
    # "start-A",
    # "start-b",
    # "A-c",
    # "A-b",
    # "b-d",
    # "A-end",
    # "b-end",
    # 19 paths:
    "dc-end",
    "HN-start",
    "start-kj",
    "dc-start",
    "dc-HN",
    "LN-dc",
    "HN-end",
    "kj-sa",
    "kj-HN",
    "kj-dc",
]


def is_small(name):
    return name.lower() == name


class Cave:
    # nodes in a cave graph
    def __init__(self, name):
        self.name = name
        self.edges = set()

    def add_edge(self, name):
        if name != self.name:
            self.edges.add(name)

    def __str__(self):
        return f"{self.name}: ({self.edges})"

    def __repr__(self):
        return f"<Cave({self.name}: ({self.edges}))>"


def get_cave_system(edges: List[str]) -> Dict[str, Cave]:
    caves = {}
    for edge in edges:
        a, b = edge.split("-")
        cave_a = caves.get(a) or Cave(a)
        cave_b = caves.get(b) or Cave(b)
        cave_a.add_edge(b)
        cave_b.add_edge(a)
        caves[a] = cave_a
        caves[b] = cave_b
    return caves


def cons(path, node):
    return (*path, node)


def is_complete(path):
    return path[-1] == "end"


def is_valid(path):
    small_caves = [node for node in path if is_small(node)]
    return (
        path[0] == "start"  # note that 'start' counts as a small cave
        and "start" not in path[1:]  # start not repeated
        and "end" not in path[:-1]  # end not repeated
        and len(set(small_caves)) == len(small_caves)
    )


def find_paths(caves, paths):
    # For each path we already know, look at the last node on the path
    # and _try to add_ all the valid paths that are path+exit
    if all(is_valid(path) and is_complete(path) for path in paths):
        return paths

    def last_cave(path):
        return caves[path[-1]]

    next_paths = {cons(path, edge) for path in paths for edge in last_cave(path).edges}

    # print(">>> path candidates:")
    # from pprint import pprint; pprint(next_paths)

    valid_paths = {path for path in next_paths if is_valid(path)}
    return valid_paths | find_paths(
        caves, {path for path in valid_paths if not is_complete(path)}
    )


def part_1(input, verbose=False):
    """
    Small caves:

    all paths you find should visit small caves at most once,
    and can visit big caves any number of times.
    """
    caves = get_cave_system(input)
    start = caves["start"]
    start_paths = {(start.name, edge) for edge in start.edges}

    # yay recursion ¯\_(ツ)_/¯
    all_paths = find_paths(caves, start_paths)

    complete_paths = {path for path in all_paths if is_complete(path)}

    if verbose:
        from pprint import pprint

        # print(">>> all paths")
        # pprint(all_paths)

        print(">>> complete paths")
        pprint(complete_paths)

    return len(complete_paths)


def part_2(input, verbose=False):
    pass


def day_12(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
