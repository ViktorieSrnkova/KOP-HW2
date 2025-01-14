#!/bin/bash

# Nastavení parametrů
set="wuf20-71/wuf20-71-"
letters=("M" "N" "Q" "R")
solutions="-opt.dat"
it=1000
et=10
cooling=0.8
eqc=1

filenames=("wuf20-0720.mwcnf" "wuf20-0420.mwcnf")

for letter in "${letters[@]}"; do
    for filename in "${filenames[@]}"; do
        echo "Processing file: $filename"
        for i in {1..50}; do
            echo "Running iteration $i for $filename"
            python3 ./Src/main.py --file "$set$letter/$filename" --solution "$set$letter$solutions" --it "$it" --et "$et" --cooling "$cooling" --eqc "$eqc"
        done
    done    
done
echo -e '\a'