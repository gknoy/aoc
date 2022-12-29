"""
# https://adventofcode.com/2022/day/7
"""
import functools
import pytest
import re
from typing import List, Union, Iterable
from utils.utils import get_line_items

input = list(get_line_items("aoc_2022/input/07.txt"))
toy_input: List[str] = [
    # fmt: off
    "$ cd /",
    "$ ls",
    "dir a",
    "14848514 b.txt",
    "8504156 c.dat",
    "dir d",
    "$ cd a",
    "$ ls",
    "dir e",
    "29116 f",
    "2557 g",
    "62596 h.lst",
    "$ cd e",
    "$ ls",
    "584 i",
    "$ cd ..",
    "$ cd ..",
    "$ cd d",
    "$ ls",
    "4060174 j",
    "8033020 d.log",
    "5626152 d.ext",
    "7214296 k",
    # fmt: on
]

CD_CMD_PATTERN = re.compile(r"^\$ cd (.+)$")
LS_CMD_PATTERN = re.compile(r"^\$ ls$")
FILE_PATTERN = re.compile(r"(\d+) (.+)$")
DIR_PATTERN = re.compile(r"dir (.+)$")

# ----------------------------------------
# Types of things we can parse:
#   - Nodes of a directory (files, directories)
#   - Commands (list files, change directory), which
#     can be duplicated for a directory
# ----------------------------------------


class ParsedItem:
    def is_cmd(self):
        return False

    def is_fs(self):
        return False


class FSNode(ParsedItem):
    """A node in the filesystems"""

    def __init__(self, name, parent=None, size=None):
        self.name = name
        self.parent = parent  # be lazy about tracking tree-parents ;)
        self._size = size
        self.children: List[FSNode] = []

    def __eq__(self, other):
        # if other is None:
        #     print(f">>> __eq__({self}, None")
        # else:
        #     print(
        #         f""">>> __eq__({self}, {other}):
        #         type(self) == type(other) ({type(self) == type(other)})
        #         and self.name == other.name  ({self.name == other.name})
        #         and self._size == other._size ({self._size == other._size})
        #         and self.children == other.children ({self.children == other.children})
        #     """
        #     )
        return (
            type(self) == type(other)
            and self.name == other.name
            and self._size == other._size
            and self.children == other.children
            # do NOT look at parent == other.parent, to prevent
            # loops ;)
        )

    def is_fs(self):
        return True

    def add_child(self, children):
        raise Exception("Cannot add children to command nodes")

    @property
    def size(self) -> int:
        if self._size is not None:
            return self._size
        self._size = 0
        for child in self.children:
            self._size += child.size
        return self._size

    def is_root(self):
        return False

    def render(self, indent: int = 2) -> str:
        indent_str = " " * indent
        if self.children:
            return f"{indent_str}- {str(self)}\n" + "\n".join(
                [child.render(indent + 2) for child in self.children]
            )
        else:
            return f"{indent_str}- {str(self)}"


class DirNode(FSNode):
    """A directory with a name + children"""

    def __repr__(self):
        return f"{self.name} (dir)"

    def is_root(self):
        return False

    def add_child(self, child):
        self._size = None  # reset size calcs
        self.children.append(child)

    def traverse(self) -> Iterable:
        """
        depth-first search of nodes
        """
        yield self
        for child in self.children:
            if isinstance(child, DirNode):
                for node in child.traverse():
                    yield node
            else:
                # only dir nodes have traverse()
                yield child


class RootDirNode(DirNode):
    """The root directly.  Has no parent / is own parent"""

    def __init__(self, name="/", parent=None, size=None):
        super(RootDirNode, self).__init__(name, parent=parent, size=size)
        self.parent = self

    def is_root(self):
        return True


class FileNode(FSNode):
    """Represent a specific child"""

    def __repr__(self):
        return f"{self.name} (file, size={self._size})"

    def add_child(self, children):
        raise Exception("Cannot add children to file")


def is_dir(node: FSNode) -> bool:
    return isinstance(node, DirNode)


class CmdNode(ParsedItem):
    """
    Commands (change dir, list contents), which are not part of the FS
    """

    def is_cmd(self):
        return True

    def is_ls(self):
        return False

    def is_cd(self):
        return False

    def __eq__(self, other):
        return type(self) == type(other) and str(self) == str(other)


class CdCommand(CmdNode):
    """Represent changing to a parent directory"""

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        return f"CMD: cd to {self.name}"

    def is_cd(self):
        return True


class LsCommand(CmdNode):
    def __repr__(self):
        return "CMD: ls"

    def is_ls(self):
        return True


# ----------------------------------------
# parsing
# ----------------------------------------


def parse_input(input: List[str]) -> RootDirNode:
    # a standalone Node, with no children
    root = RootDirNode("/")
    root.parent = root  # in case some jerk decides to 'cd ..' too many times
    current = root
    # now, for each line, build our tree
    for line in input:
        node = parse_line(line, current_node=current)
        if node.is_cmd():
            node: CmdNode = node
            if node.is_cd():
                node: CdCommand = node
                if node.name == "/":
                    current = root
                elif node.name == "..":
                    current = current.parent
                else:
                    # we are cd into a subdir of current
                    cd_targets = [
                        child
                        for child in current.children
                        if is_dir(child) and child.name == node.name
                    ]
                    assert 1 == len(cd_targets)
                    current = cd_targets[0]
            if node.is_ls():
                # This is exploitable if input does ls but never lists files,
                # but we assume input isn't trying to exploit, and will
                # have subsequent lines that show file/dir entries
                current.children.clear()
        if node.is_fs():
            # add directories when we see them, NOT when we cd into them
            current.add_child(node)

    return root


def parse_line(raw_input: str, current_node=None) -> ParsedItem:
    file_match = FILE_PATTERN.match(raw_input)
    if file_match:
        size, name = file_match.groups()
        return FileNode(name=name, parent=current_node, size=int(size))
    cd_match = CD_CMD_PATTERN.match(raw_input)
    if cd_match:
        # unpack
        name, = cd_match.groups()
        if name == "..":
            # Return something different so that we know NOT to put in tree
            # We don't care
            return CdCommand(name="..")
        return CdCommand(name=name)
    ls_match = LS_CMD_PATTERN.match(raw_input)
    if ls_match:
        return LsCommand()
    dir_match = DIR_PATTERN.match(raw_input)
    if dir_match:
        [name] = dir_match.groups()
        return DirNode(name, parent=current_node)

    # if we get here, something is wrong
    raise Exception(f"Cannot match input: {raw_input}")


# ----------------------------------------
# tests
# ----------------------------------------


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


# ----------------------------------------
# Part 1:   Find all of the directories with a total size of at most 100000,
#           then calculate the sum of their total sizes.
# ----------------------------------------


def part_1(input, verbose=False):
    """
    Given the commands and output in the example above, you can determine that
    the filesystem looks visually like this:

        - / (dir)
          - a (dir)
            - e (dir)
              - i (file, size=584)
            - f (file, size=29116)
            - g (file, size=2557)
            - h.lst (file, size=62596)
          - b.txt (file, size=14848514)
          - c.dat (file, size=8504156)
          - d (dir)
            - j (file, size=4060174)
            - d.log (file, size=8033020)
            - d.ext (file, size=5626152)
            - k (file, size=7214296)

    ... you need to determine the total size of each directory.

    Find all of the directories with a total size of at most 100000,
    then calculate the sum of their total sizes.
    In the example above, these directories are a and e;
    the sum of their total sizes is 95437 (94853 + 584).
    (As in this example, this process can count files more than once!)

    NOTES ON INPUT:
    We cd into the same-named directory several times. Not sure yet if these are
    duplicates that have the same parent (e.g., cd foo, cd .., cd foo),
    or have different parents (e.g., cd foo, cd foo).

        $ ag cd aoc_2022/input/07.txt | cut -c 10- | sort | uniq -c | sort
           2 cqnblb
           6 zprprf
           8 dcqnblb
           9 ldzslndn
           9 qcq
          14 dqp
          15 .
         157 ..

    """
    root = parse_input(input)
    if verbose:
        print(">>> Part 1:")
        print(root.render(2))
    # trigger all size calcs ;)
    root.size

    small_dirs = [
        item
        for item in root.traverse()
        if item.size <= 100000 and item != root and is_dir(item)
    ]
    if verbose:
        print(f"    small dirs: {small_dirs}")
    return sum(item.size for item in small_dirs)


def part_2(input, verbose=False):
    """
    max space is 70000000
    You need unused space of at least 30000000.

    Directories e and a are both too small;
    deleting them would not free up enough space.
    However, directories d and / are both big enough! Between these,
    choose the smallest: d, increasing unused space by 24933642.

    Find the smallest directory that, if deleted, would free up enough space on
    the filesystem to run the update. What is the total size of that directory?
    """
    max_space = 70000000
    min_free = 30000000

    #  |....1....2....3....4....5....6....7|
    #  |-----------------------------------|  max_space
    #  |                   |xxxxxxxxxxxxxxx|  min_free
    #  |===========================|.......|  orig_size
    #  |                           |<----->|  orig_free
    #  |                   |xxxxxxx|       |  min_deletable_size
    #
    # The device is already TOO FULL, so we know that orig_free < min_free (!)
    # So, we need to find the smallest directory that is >= min_deletable_size

    root = parse_input(input)
    orig_size = root.size
    orig_free = max_space - orig_size
    min_deletable_size = min_free - orig_free

    deletable_dirs = [
        item
        for item in root.traverse()
        if is_dir(item) and item.size >= min_deletable_size
    ]

    def pick_smaller(a, b):
        return a if a.size < b.size else b

    smallest_deletable_dir = functools.reduce(
        pick_smaller, deletable_dirs, deletable_dirs[0]
    )

    if verbose:
        print(
            f""">>> Part 2:
        max_space: {max_space}
        min_free: {min_free}
        orig_size: {orig_size}
        orig_free: {orig_free}
        deletable_dirs: {deletable_dirs}
        smallest: {smallest_deletable_dir}
        smallest_size: {smallest_deletable_dir.size}
        """
        )
        pass

    return smallest_deletable_dir.size


def day_7(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
