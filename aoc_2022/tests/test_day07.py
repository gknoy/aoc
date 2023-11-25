"""
# https://adventofcode.com/2022/day/7
"""
import pytest
from typing import Union

from aoc_2022.days.day07 import (
    input,
    toy_input,
    part_1,
    part_2,
    parse_line,
    parse_input,
    CdCommand,
    DirNode,
    FileNode,
    FSNode,
    LsCommand,
    ParsedItem,
    RootDirNode,
)


@pytest.mark.parametrize(
    "line,expected",
    [
        ["waffles", Exception("Cannot match input: waffles")],
        ["$ cd /", CdCommand("/")],
        ["$ cd ..", CdCommand("..")],
        ["$ cd foo", CdCommand("foo")],
        ["$ ls", LsCommand()],
        ["dir a", DirNode("a")],
        ["14848514 b.txt", FileNode("b.txt", size=14848514)],
        ["29116 f", FileNode("f", size=29116)],
    ],
)
def test_parse_line(line: str, expected: Union[Exception, ParsedItem]):
    current = DirNode("current", parent=RootDirNode("/"))
    if type(expected) is Exception:
        with pytest.raises(Exception) as raised:
            parse_line(line, current_node=current)
        assert raised.match(str(expected))
    else:
        expected: ParsedItem = expected
        parsed = parse_line(line, current_node=current)
        assert parsed == expected
        if expected.is_fs():
            assert parsed.parent == current
            assert parsed.size == expected.size


def test_size():
    root = RootDirNode()
    a = DirNode(name="a", parent=root)
    e = DirNode(name="e", parent=a)
    e.add_child(FileNode(name="i", size=584, parent=e))
    a.add_child(e)
    a.add_child(FileNode(name="f", size=29116, parent=a))
    a.add_child(FileNode(name="g", size=2557, parent=a))
    a.add_child(FileNode(name="h.lst", size=62596, parent=a))
    root.add_child(a)
    root.add_child(FileNode(name="b.txt", size=14848514, parent=root))
    root.add_child(FileNode(name="c.dat", size=8504156, parent=root))
    d = DirNode(name="d", parent=root)
    d.add_child(FileNode(name="j", size=4060174, parent=d))
    d.add_child(FileNode(name="d.log", size=8033020, parent=d))
    d.add_child(FileNode(name="d.ext", size=5626152, parent=d))
    d.add_child(FileNode(name="k", size=7214296, parent=d))
    root.add_child(d)
    assert e.size == 584
    assert a.size == e.size + 29116 + 2557 + 62596
    assert d.size == 4060174 + 8033020 + 5626152 + 7214296
    assert root.size == a.size + 14848514 + 8504156 + d.size


@pytest.fixture
def expected_toy_tree():
    # Expected root from part 1 problem description
    root = RootDirNode()
    a = DirNode(name="a", parent=root)
    e = DirNode(name="e", parent=a)
    e.add_child(FileNode(name="i", size=584, parent=e))
    a.add_child(e)
    a.add_child(FileNode(name="f", size=29116, parent=a))
    a.add_child(FileNode(name="g", size=2557, parent=a))
    a.add_child(FileNode(name="h.lst", size=62596, parent=a))
    root.add_child(a)
    root.add_child(FileNode(name="b.txt", size=14848514, parent=root))
    root.add_child(FileNode(name="c.dat", size=8504156, parent=root))
    d = DirNode(name="d", parent=root)
    d.add_child(FileNode(name="j", size=4060174, parent=d))
    d.add_child(FileNode(name="d.log", size=8033020, parent=d))
    d.add_child(FileNode(name="d.ext", size=5626152, parent=d))
    d.add_child(FileNode(name="k", size=7214296, parent=d))
    root.add_child(d)
    return root


def test_parse_input(expected_toy_tree):
    parsed = parse_input(toy_input)
    assert parsed.render() == expected_toy_tree.render()
    assert parsed == expected_toy_tree


def test_traverse(expected_toy_tree):
    items = list(expected_toy_tree.traverse())
    for item in items:
        assert isinstance(item, FSNode)
    assert [item.name for item in items] == [
        "/",
        "a",
        "e",
        "i",
        "f",
        "g",
        "h.lst",
        "b.txt",
        "c.dat",
        "d",
        "j",
        "d.log",
        "d.ext",
        "k",
    ]


def test_part_1_toy():
    assert part_1(toy_input) == 95437


def test_part_1_real():
    assert part_1(input) == 1844187


def test_part_2_toy():
    assert part_2(toy_input) == 24933642


def test_part_2_real():
    assert part_2(input) == 4978279
