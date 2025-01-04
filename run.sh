#!/bin/bash

# Nastavení parametrů
base_dir="Data"
set="wuf20-71/wuf20-71-M"
folder="$base_dir/$set"
solutions="$set-opt.dat"  # Correct solution file path
it=100
et=10
cooling=0.8
eqc=1.0

# Spuštění Python skriptu pro všechny soubory v dané složce
for filename in ./$folder/*.mwcnf; do
    f=$(basename "$filename")
    echo "Processing file: $f"
    python3 ./Src/main.py --file "$set/$f" --solution "$solutions" --it "$it" --et "$et" --cooling "$cooling" --eqc "$eqc"
done
