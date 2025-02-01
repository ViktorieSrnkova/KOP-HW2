#!/bin/bash

# Nastavení parametrů
set="Data/wuf50-218R/wuf50-218R-"
letters=("M" "N" "Q" "R")
solutions="-opt.dat"
it=63
et=0.75
cooling=0.976
eqc=12

for letter in "${letters[@]}"; do
    folder="$set$letter"
    items=$(ls "$folder")
    for item in $items; do
        filepath="$folder/$item"
        for i in {1..1}; do
            echo "Running iteration $i for $filepath"
            python3 ./Src/main.py --file "$filepath" --solution "$folder$solutions" --it "$it" --et "$et" --cooling "$cooling" --eqc "$eqc"
        done
    done    
done
#echo -e '\a'