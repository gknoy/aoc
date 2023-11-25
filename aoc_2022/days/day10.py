"""
# https://adventofcode.com/2022/day/10
"""
import itertools
from dataclasses import dataclass
from utils.utils import get_line_items

input = list(get_line_items("aoc_2022/input/10.txt"))
toy_input: list[str] = [
    # fmt: off
    "addx 15",
    "addx -11",
    "addx 6",
    "addx -3",
    "addx 5",
    "addx -1",
    "addx -8",
    "addx 13",
    "addx 4",
    "noop",
    "addx -1",
    "addx 5",
    "addx -1",
    "addx 5",
    "addx -1",
    "addx 5",
    "addx -1",
    "addx 5",
    "addx -1",
    "addx -35",
    "addx 1",
    "addx 24",
    "addx -19",
    "addx 1",
    "addx 16",
    "addx -11",
    "noop",
    "noop",
    "addx 21",
    "addx -15",
    "noop",
    "noop",
    "addx -3",
    "addx 9",
    "addx 1",
    "addx -3",
    "addx 8",
    "addx 1",
    "addx 5",
    "noop",
    "noop",
    "noop",
    "noop",
    "noop",
    "addx -36",
    "noop",
    "addx 1",
    "addx 7",
    "noop",
    "noop",
    "noop",
    "addx 2",
    "addx 6",
    "noop",
    "noop",
    "noop",
    "noop",
    "noop",
    "addx 1",
    "noop",
    "noop",
    "addx 7",
    "addx 1",
    "noop",
    "addx -13",
    "addx 13",
    "addx 7",
    "noop",
    "addx 1",
    "addx -33",
    "noop",
    "noop",
    "noop",
    "addx 2",
    "noop",
    "noop",
    "noop",
    "addx 8",
    "noop",
    "addx -1",
    "addx 2",
    "addx 1",
    "noop",
    "addx 17",
    "addx -9",
    "addx 1",
    "addx 1",
    "addx -3",
    "addx 11",
    "noop",
    "noop",
    "addx 1",
    "noop",
    "addx 1",
    "noop",
    "noop",
    "addx -13",
    "addx -19",
    "addx 1",
    "addx 3",
    "addx 26",
    "addx -30",
    "addx 12",
    "addx -1",
    "addx 3",
    "addx 1",
    "noop",
    "noop",
    "noop",
    "addx -9",
    "addx 18",
    "addx 1",
    "addx 2",
    "noop",
    "noop",
    "addx 9",
    "noop",
    "noop",
    "noop",
    "addx -1",
    "addx 2",
    "addx -37",
    "addx 1",
    "addx 3",
    "noop",
    "addx 15",
    "addx -21",
    "addx 22",
    "addx -6",
    "addx 1",
    "noop",
    "addx 2",
    "addx 1",
    "noop",
    "addx -10",
    "noop",
    "noop",
    "addx 20",
    "addx 1",
    "addx 2",
    "addx 2",
    "addx -6",
    "addx -11",
    "noop",
    "noop",
    "noop",
    # fmt: on
]


# --------------------------------
# Part 1
# --------------------------------
# - single register computer
# - `addx V` takes two cycles to complete.
#               After two cycles, the X register is increased by the value V. (V can be negative.)
#               In first cycle, no changes
# - `noop` takes one cycle to complete. It has no other effect.

# instruction functions -- generate a thing that acts on register


def noop() -> callable:
    def _noop(register) -> callable:
        # do nothing
        yield register.value

    return _noop


def addx(v) -> callable:
    def add_x(register):
        # two cycles, no change in first cycle
        yield register.value
        register.value += v
        yield register.value

    return add_x


def parse_line(line) -> callable:
    tokens = line.split(" ")
    match tokens[0]:
        case "noop":
            return noop()
        case "addx":
            return addx(int(tokens[1]))
    raise Exception(f"Bad input: {line}")


def parse_input(lines):
    return (parse_line(line) for line in lines)


def signal_strength(cycle: int, register: int) -> int:
    return cycle * register


@dataclass
class Register:
    name: str
    value: int = 1

    def __str__(self):
        return f"{self.name}: {self.value}"


class Cpu_v1:
    def __init__(self):
        self.x: Register = Register("x", 1)
        self.max_cycles: int = 1000
        self.signal_strengths: dict = {}
        self.min_interesting_cycle: int = 20
        self.interesting_cycle_interval: int = 40

    def is_interesting_cycle(self, cycle) -> bool:
        return (cycle == self.min_interesting_cycle) or (
            cycle > self.min_interesting_cycle
            and (cycle - self.min_interesting_cycle) % self.interesting_cycle_interval
            == 0
        )

    def process(self, instructions, verbose=False):
        # TODO: refactor if we ever have more than one register ;)
        instructions_on_registers = (
            instruction(self.x) for instruction in instructions
        )
        cycle_ops = itertools.chain.from_iterable(instructions_on_registers)
        cycle = 1
        while cycle < self.max_cycles:
            try:
                next(cycle_ops)
                cycle += 1
                if verbose:
                    print(f"{cycle} -- {self.x}")
                if self.is_interesting_cycle(cycle):
                    if verbose:
                        print(f" --> signal: {signal_strength(cycle, self.x.value)}")
                    self.signal_strengths[cycle] = signal_strength(cycle, self.x.value)
            except StopIteration:
                # done with instructions so nothing more to do
                return


def part_1(input, verbose=False):
    instructions = parse_input(input)  # this is a list of callables
    cpu = Cpu_v1()
    cpu.process(instructions, verbose=verbose)
    if verbose:
        print(f"Signal strengths: {cpu.signal_strengths}")
    return sum(cpu.signal_strengths.values())


# --------------------------------
# Part 2
# --------------------------------


def part_2(input, verbose=False):
    pass


def day_10(use_toy_data=False, verbose=False):
    data = toy_input if use_toy_data else input
    return [part_1(data, verbose), part_2(data, verbose)]
