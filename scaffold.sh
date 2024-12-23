#!/bin/bash
#
# scaffold.sh
#
# Generate new input + script modules for dayNN
#

YEAR="$1"
N="$2"
NN=`printf %02d $N`

NEW_FILE="aoc_${YEAR}/days/day${NN}.py"
NEW_TEST_FILE="aoc_${YEAR}/tests/test_day${NN}.py"

cp "aoc_${YEAR}/days/template.py" "${NEW_FILE}"
cp "aoc_${YEAR}/tests/template.py" "${NEW_TEST_FILE}"
sed -i '' "s/NN/${NN}/g; s/N/${N}/g;" "${NEW_FILE}"
sed -i '' "s/{NN}/${NN}/g; s/{N}/${N}/g;" "${NEW_TEST_FILE}"

# Pre-get input data so we can read it and look at it, but 
# 2024+ will now just use aocd directly in the day module.
aocd "${YEAR}" "${N}" > "aoc_${YEAR}/input/${NN}.txt"