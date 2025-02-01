#!/bin/bash

# Nastavení parametrů
base_dir="Data"
set="Data/wuf75-325/wuf75-325-R"
folder="$base_dir/$set"
solutions="$set-opt.dat"  # Correct solution file path
it=63
et=0.75
cooling=0.976
eqc=10
# Specify the file to run
filenames=("wuf75-021.mwcnf")
# "wuf20-050.mwcnf" "wuf20-061.mwcnf" "wuf20-063.mwcnf" "wuf20-073.mwcnf
# "wuf20-012.mwcnf" "wuf20-021.mwcnf" "wuf20-031.mwcnf" "wuf20-013.mwcnf"
#filename1="wuf20-0145.mwcnf"
#filename2="wuf20-0778.mwcnf"

# Process the specified file

for filename in "${filenames[@]}"; do
    echo "Processing file: $filename"
    for i in {1..5}; do
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