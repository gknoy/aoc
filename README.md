# aoc

Advent of Code 2023

cf. https://adventofcode.com/2023/

### Pre-requisites / Starting:

My recent 2022 puzzles use features from python 3.11 (for nicer type hinting).

```sh
pyenv install 3.11.4
pyenv local 3.11.4
pip install -r requirements.txt
```

I'm building this on a Macbook with `pyenv` installed, and 
haven't yet gotten things working on my pc. ;)

### Avoiding Spoilers

If you clone this and start working after I've already started playing, 
you could see my solutions. ;)  You probably don't want that, so you probably 
want to delete my solutions + tests and diverge from main:

```sh
git checkout main

# delete solutions to prevent spoilers
rm aoc_2023/days/day*.py
rm aoc_2023/input/*.txt
rm aoc_2023/days/test*.py

git add aoc_2023/
git commit -m "DIVERGE from gknoy/aoc:main to avoid spoilers"

# get started on day 1 :D
git checkout main -b 2023-01
```

This has the advantage of keeping any tooling fixes that I make since Dec 1.

### Starting a new day's puzzle

Check out a new branch, and run `scaffold.sh` to create files for day N:
```sh
git checkout main -b 2023-01

# ./scaffold.sh {year} {day} 
./scaffold.sh 2023 1
```

```
aoc_2023/days/day{NN}.py        # day N's puzzle solution
aoc_2023/input/{NN}.txt         # your input for day N
aoc_2023/tests/test_day{NN}.py  # tests that verify that your solution works
```

Paste your puzzle input (which is the same for part 1 and part 2) 
into `aoc_2023/input/{NN}.txt`.

Paste the "example" input into the `TOY_INPUT` list (one string per line of input).
For example, for Day 1, you would edit `aoc_2023/days/day01.py`:
```py
input = list(get_line_items("aoc_2023/input/01.txt"))
toy_input: list[str] = [
    # fmt: off
    "1abc2",
    "pqr3stu8vwx",
    "a1b2c3d4e5f",
    "treb7uchet",
    # fmt: on
]
```

You should then add the toy example's expected value to day 1's tests for part 1 with toy input:

> In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

```py
def test_part_1_toy():
    assert part_1(toy_input) == 142
```
(You can write tests directly in the `day01.py` file, but it's considered better practice to put them in a separate file.)

### Running daily puzzle scripts

Run day 1's script:

```sh
./aoc.py 2023 1
# or
./aoc.py 2023 1 --toy --verbose
```
You can use `--toy` or `--verbose` flags to set values that will automatically affect which `input` values are passed to your `part_1`/`part_2` functions in your `dayNN.py` script.

The output printed is a list of the part 1 and part 2 solutions.  

For example, my solutions from last year:
```sh
$ ./aoc.py 2022 9
2022  9: [6486, 2678]

# if you leave off the day, it will run all for that year
$ ./aoc.py 2022
2022  1: [70296, 205381]
2022  2: [10404, 10334]
2022  3: [7831, 2683]
# ....
```

### Running Tests

Tests should be run with `pytest`, and verifies toy solutions and real solutions.
Some days' solutions have one-off sanity check tests that I used for making 
sure helpers worked as expected, but do not need to be run as part of the 
test suite.  

```python
# all tests for 2023:
pytest aoc_2023/

# just today's test:
pytest aoc_2023/tests/test_day01.py

# just one test:
pytest aoc_2023/tests/test_day01.py::test_part_1_toy
```
