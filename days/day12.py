"""
# Passage Pathing
# https://adventofcode.com/2021/day/12
"""
from functools import cached_property
from typing import Dict, List
from utils import get_line_items

input = list(get_line_items("input/12.txt"))
toy_input: List[str] = [
    # Looks like:
    #      start
    #      /   \
    #  c--A-----b--d
    #      \   /
    #       end
    "start-A",
    "start-b",
    "A-c",
    "A-b",
    "b-d",
    "A-end",
    "b-end",
]



def is_large(name):
    return name.to_upper() == name


def is_small(name):
    return name.to_lower() == name


class Cave:
    # nodes in a cave graph
    def __init__(self, name):
        self.name = name
        self.edges = set()

    @cached_property
    def is_small(self):
        return self.name.to_lower() == self.name

    @cached_property
    def is_large(self):
        return self.name.to_upper() == self.name

    @cached_property
    def is_start(self):
        return self.name == "start"

    @cached_property
    def is_end(self):
        return self.name == "end"

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


def find_paths_visiting_small_caves_only_once(caves):
    paths = set()
    start = caves["start"]
    end = caves["end"]


def part_1(input, verbose=False):
    """
    Small caves:

    all paths you find should visit small caves at most once,
    and can visit big caves any number of times.
    """
    caves = get_cave_system(input)
    start = caves["start"]
    end = caves["end"]


    pass


def part_2(input, verbose=False):
    pass


def day_12(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
