"""
# https://adventofcode.com/2021/day/5
"""
import pytest
from utils import get_line_items

input = list(get_line_items("input/05.txt"))
toy_input = [
    "0,9 -> 5,9",
    "8,0 -> 0,8",
    "9,4 -> 3,4",
    "2,2 -> 2,1",
    "7,0 -> 7,4",
    "6,4 -> 2,0",
    "0,9 -> 2,9",
    "3,4 -> 1,4",
    "0,0 -> 8,8",
    "5,5 -> 8,2",
]

expected_maps = {
    1: """.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....""",
    2: None,
}


def parse_input(lines):
    """
    return pairs of tuples for each line
    e.g.
        [[(0, 9), (5, 9)],
         [(8, 0), (0, 8)], ... ]
    """
    return [
        [tuple(map(int, pair.split(","))) for pair in line.split(" -> ")]
        for line in lines
    ]


def interpolate(a, b):
    """
    Get all the points on a line between a and b,
    accounting for slope between a and b
    """
    delta_x = b[0] - a[0]
    delta_y = b[1] - a[1]

    if delta_x == 0:
        # it's a vertical line at a[0] from a[1] to b[1]
        step = 1 if delta_y > 0 else -1
        return [(a[0], y) for y in range(a[1], b[1] + step, step)]

    slope = delta_y / delta_x if delta_x != 0 else 0
    # b can be leftward of a:
    step = 1 if (a[0] < b[0]) else -1

    def f(x):
        # point on line (segment) intersecting A and B
        return int(a[1] + slope * (x - a[0]))

    return [(x, f(x)) for x in range(a[0], b[0] + step, step)]


@pytest.mark.parametrize(
    "a,b,expected",
    [
        [(0, 0), (2, 2), [(0, 0), (1, 1), (2, 2)]],
        [(2, 2), (0, 0), [(0, 0), (1, 1), (2, 2)]],
        [(0, 2), (2, 0), [(0, 2), (1, 1), (2, 0)]],
        [(2, 0), (0, 2), [(0, 2), (1, 1), (2, 0)]],
        [(0, 0), (2, 0), [(0, 0), (1, 0), (2, 0)]],
        # vertical:
        [(0, 0), (0, 2), [(0, 0), (0, 1), (0, 2)]],
    ],
)
def test_interpolate(a, b, expected):
    assert sorted(interpolate(a, b)) == expected


def is_vertical_or_horizontal(line):
    a, b = line
    return (a[0] == b[0]) or (a[1] == b[1])


class Grid:
    def __init__(self, data, orthogonal_only=False):
        # data are pairs of tuples.
        # TODO: optimize this to not loop 4x ;)
        self.data = data
        self.orthogonal_only = orthogonal_only
        self.min_x = min(point[0] for segment in data for point in segment) or 0
        self.min_y = min(point[1] for segment in data for point in segment) or 0
        self.max_x = max(point[0] for segment in data for point in segment)
        self.max_y = max(point[1] for segment in data for point in segment)

        self.grid = [
            [0 for y in range(self.min_y, self.max_y + 1)]
            for x in range(self.min_x, self.max_x + 1)
        ]

    def populate(self):
        for line in self.data:
            if self.orthogonal_only:
                if is_vertical_or_horizontal(line):
                    self.add_line(line)
            else:
                self.add_line(line)

    def add_line(self, line):
        for point in interpolate(*line):
            self.grid[point[0]][point[1]] += 1

    def score(self, min_overlap):
        # how many points have {min_overlap} lines overlapping
        count = 0
        for row in self.grid:
            for col in row:
                if col >= min_overlap:
                    count += 1
        return count

    def __str__(self):
        """Pretty-print with selected numbers in bold"""
        row_strings = [
            "".join(
                [
                    self.render_item(self.grid[x][y])
                    for x in range(self.min_x, self.max_x + 1)
                ]
            )
            for y in range(self.min_y, self.max_y + 1)
        ]
        return "\n".join(row_strings)

    def render_item(self, item):
        # TODO: bold if at least two intersect
        return "." if item == 0 else str(item)


def part_1(input, verbose=False):
    grid = Grid(input, orthogonal_only=True)
    grid.populate()
    if verbose:
        print(grid)
    return grid.score(min_overlap=2)


def part_2(input, verbose=False):
    grid = Grid(input)
    return None


def day_5(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    data = parse_input(data)
    return [part_1(data, verbose), part_2(data, verbose)]
