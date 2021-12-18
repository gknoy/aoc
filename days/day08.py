"""
# https://adventofcode.com/2021/day/8
"""
from utils import get_line_items

input = list(get_line_items("input/08.txt"))
toy_input = [
    "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
    "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
    "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",
    "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",
    "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",
    "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",
    "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",
    "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",
    "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",
    "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce",
]


def parse_line(line):
    input, output = line.split(" | ")
    return [input.split(), output.split()]


def parse_lines(data):
    return [parse_line(line) for line in data]


def canonical(signal):
    """Unscramble order of wires, e.g ceb -> bce"""
    return "".join(sorted(signal))


# EASY_DIGITS_LENGTHS = {
#     # len: value
#     2: 1,
#     3: 7,
#     4: 4,
#     7: 8,
# }

# FIXME REMOVE: For validation
UNSCRAMBLED = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}


def render_wire(wire, wires, blank=" "):
    return wire if wire in set(wires) else blank


def render(wires):
    if wires.startswith("--"):
        print(wires)
        return
    a = render_wire("a", wires)
    b = render_wire("b", wires)
    c = render_wire("c", wires)
    d = render_wire("d", wires)
    e = render_wire("e", wires)
    f = render_wire("f", wires)
    g = render_wire("g", wires)

    print(
        f"""
      {a*4}
     {b}    {c}
     {b}    {c}
      {d*4}
     {e}    {f}
     {e}    {f}
      {g*4}
    """
    )


def contains_segment(a, b):
    return set(b) & set(a) == set(b)


def filter_items_containing(items, segments):
    return [item for item in items if contains_segment(item, segments)]


def deduce_digits_from_signals(signals, verbose=False):
    """
    Transform a list of signals like [be, cfbegad, cbdgef, fgaecd, cgeb, fdcge, agebfd, fecdb, fabcd, edb, ]
    into digits mapping

    0:      1:      2:      3:      4:
     aaaa    ....    aaaa    aaaa    ....
    b    c  .    c  .    c  .    c  b    c
    b    c  .    c  .    c  .    c  b    c
     ....    ....    dddd    dddd    dddd
    e    f  .    f  e    .  .    f  .    f
    e    f  .    f  e    .  .    f  .    f
     gggg    ....    gggg    gggg    ....

    5:      6:      7:      8:      9:
     aaaa    aaaa    aaaa    aaaa    aaaa
    b    .  b    .  .    c  b    c  b    c
    b    .  b    .  .    c  b    c  b    c
     dddd    dddd    ....    dddd    dddd
    .    f  e    f  .    f  e    f  .    f
    .    f  e    f  .    f  e    f  .    f
     gggg    gggg    ....    gggg    gggg

    mapping:
    {
        "be": 1,
        1: "be",  # etc
    }
    """

    # ['be',      # -> 1
    #  'bde',     # -> 7
    #  'bceg',    # -> 4
    #  'cdefg',   # \
    #  'bcdef',   #  (2, 3, 5)
    #  'abcdf',   # /
    #  'bcdefg',  # \
    #  'acdefg',  #  (0, 6, 9)
    #  'abdefg',  # /
    #  'abcdefg'  # -> 8
    # ]
    signals_sorted_by_size = sorted(signals, key=lambda x: len(x))

    # easy ones
    one = signals_sorted_by_size[0]
    seven = signals_sorted_by_size[1]
    four = signals_sorted_by_size[2]
    eight = signals_sorted_by_size[9]

    five_wires = signals_sorted_by_size[3:6]  # 2, 3, 5
    six_wires = signals_sorted_by_size[6:9]  # 0, 6, 9

    # based on the easy digits' wires, we can deduce the others based on ascii art

    three = filter_items_containing(five_wires, one)[0]
    nine = canonical(set(three) | set(four))

    b_segment = set(nine) ^ set(three)
    five = filter_items_containing(five_wires, b_segment)[0]

    horizontal_segments = set(three) ^ set(one)
    six = [
        item
        for item in six_wires
        if item != nine and contains_segment(item, horizontal_segments)
    ][0]

    two = [item for item in five_wires if item not in [three, five]][0]
    zero = [item for item in six_wires if item not in [six, nine]][0]

    digits_map = {
        0: zero,
        1: one,
        2: two,
        3: three,
        4: four,
        5: five,
        6: six,
        7: seven,
        8: eight,
        9: nine,
        zero: 0,
        one: 1,
        two: 2,
        three: 3,
        four: 4,
        five: 5,
        six: 6,
        seven: 7,
        eight: 8,
        nine: 9,
    }

    if verbose:
        for digit in range(10):
            print(f">>> {digit}:")
            render(digits_map[digit])

    return digits_map


def translate(outputs, digits_map):
    return [digits_map[item] for item in outputs]


def translate_line(line):
    inputs = list(map(canonical, line[0]))
    outputs = list(map(canonical, line[1]))

    digits_map = deduce_digits_from_signals(inputs)
    output_digits = translate(outputs, digits_map)
    return digits_map, output_digits


def map_multiple(fns, iterable):
    return []


def part_1(input, verbose=False):
    data = parse_lines(input)

    if verbose:
        fake_line = [item for item in UNSCRAMBLED if type(item) is str]
        deduce_digits_from_signals(fake_line, verbose=verbose)

    def count_easy_digits(digits, output):
        easy_digits = {1, 7, 4, 8}
        return sum(1 for item in output if item in easy_digits)

    return sum(
        count_easy_digits(*translated) for translated in map(translate_line, data)
    )


def part_2(input, verbose=False):
    data = parse_lines(input)

    if verbose:
        fake_line = [item for item in UNSCRAMBLED if type(item) is str]
        deduce_digits_from_signals(fake_line, verbose=verbose)

    def concat_digits(digits, output):
        """[1, 2, 3, 4] -> 1234"""
        return int("".join(map(str, output)))

    return sum(concat_digits(*translated) for translated in map(translate_line, data))


def day_8(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
