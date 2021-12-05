#!/bin/bash
#
# scaffold.sh
#
# Generate new input + script modules for dayNN
#

N="$1"
NN=`printf %02d $N`

NEW_FILE="days/day${NN}.py"

touch "input/${NN}.txt"
cp days/day_template.py "${NEW_FILE}"
sed -i '' "s/NN/${NN}/g; s/N/${N}/g;" "${NEW_FILE}"

# git add "$NEW_FILE" "input/${NN}.txt"
