#!/bin/bash

# Nastavení parametrů
set="wuf75-325/wuf75-325-"
letters=("M" "N" "Q" "R")
solutions="-opt.dat"
it=1000
et=10
cooling=0.8
eqc=1

filename="wuf75-01.mwcnf"

for letter in "${letters[@]}"; do
    echo "Processing file: $filename"
    for i in {1..100}; do
        echo "Running iteration $i for $filename"
        python3 ./Src/main.py --file "$set$letter/$filename" --solution "$set$letter$solutions" --it "$it" --et "$et" --cooling "$cooling" --eqc "$eqc"
    done
done
echo -e '\a'