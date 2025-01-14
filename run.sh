#!/bin/bash

# Nastavení parametrů
base_dir="Data"
set="wuf20-91/wuf20-91-M"
folder="$base_dir/$set"
solutions="$set-opt.dat"  # Correct solution file path
it=100
et=10
cooling=0.8
eqc=1

# Specify the file to run
filenames=("wuf20-010.mwcnf" "wuf20-011.mwcnf" "wuf20-012.mwcnf" "wuf20-013.mwcnf" "wuf20-014.mwcnf")
#filename1="wuf20-0145.mwcnf"
#filename2="wuf20-0778.mwcnf"

# Process the specified file

for filename in "${filenames[@]}"; do
    echo "Processing file: $filename"
    for i in {1..100}; do
        echo "Running iteration $i for $filename"
        python3 ./Src/main.py --file "$set/$filename" --solution "$solutions" --it "$it" --et "$et" --cooling "$cooling" --eqc "$eqc"
    done
done
echo -e '\a'
#echo "Processing file: $filename"
#python3 ./Src/main.py --file "$set/$filename" --solution "$solutions" --it "$it" --et "$et" --cooling "$cooling" --eqc "$eqc"

#echo "Processing file: $filename"
#python3 ./Src/main.py --file "$set/$filename1" --solution "$solutions" --it "$it" --et "$et" --cooling "$cooling" --eqc "$eqc"
#
#echo "Processing file: $filename"
#python3 ./Src/main.py --file "$set/$filename2" --solution "$solutions" --it "$it" --et "$et" --cooling "$cooling" --eqc "$eqc"