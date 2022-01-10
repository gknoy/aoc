# advent2021

Advent of code 2021

cf. https://adventofcode.com/2021/

### Invocation

Invoke `advent.py` with the advent day:

```bash
# pyenv local 3.9.6

./advent.py 1
# or
./advent.py 9 --toy --verbose
# or
./advent.py --all

```

### Tests

Tests should be run with `pytest`, and verifies toy solutions and real solutions.
Some days' solutions have one-off sanity check tests that I used for making 
sure helpers worked as expected, but do not need to be run as part of the 
test suite.  

```python
pytest .
```

### Scaffolding a new day's solution

Use `scaffold.sh` to create a blank solution template + input file

```bash
./scaffold.sh 13
# creates
#	days/day13.py
#	input/13.txt
```

After creating these, one must still import that day's solution in `advent.py`:
```python
from days.day13 import day_13
``` 
These imports are used to autodetect solutions. 
I want to make this more automated with importlib, but haven't bothered yet 
with the extra complexity of figuring that out.

One must also add a line of expected test values in `test_advents.py`:
```python
TOY_EXPECTED = {
    # ....
    13: [17, None],  
    # ^^^ note no toy value for part 2 until I solve part 1
}


EXPECTED = {
    # ....
    13: [None, None],  
    # ^^^ fix these once we succeed at a solution
}
```
