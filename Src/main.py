import argparse
import os
from pathlib import Path
from parser import Instance, Solutions
from solver import Solver
import csv

class Input:
    def __init__(self, file, solution, it, et, cooling, eq_coefficient):
        self.file = file
        self.solution = solution
        self.it = it
        self.et = et
        self.cooling = cooling
        self.eq_coefficient = eq_coefficient

def get_input():
    parser = argparse.ArgumentParser(description="KOP - Simulated Annealing for MWSAT")
    parser.add_argument(
        "--file",
        type=str,
        default="wuf20-71/wuf20-71-M/wuf20-01.mwcnf",  # Adjusted for your file structure
        help="Path to instance in folder /data (default: wuf20-71/wuf20-71-M/wuf20-01.mwcnf)"
    )
    parser.add_argument(
        "--solution",
        type=str,
        default="wuf20-71/wuf20-71-M-opt.dat",  # Adjusted for your file structure
        help="Filename of input solution (default: wuf20-71/wuf20-71-M-opt.dat)"
    )
    parser.add_argument(
        "--it",
        type=int,
        default=100,
        help="Initial temperature (default: 100)"
    )
    parser.add_argument(
        "--et",
        type=int,
        default=10,
        help="Freeze temperature (default: 10)"
    )
    parser.add_argument(
        "--cooling",
        type=float,
        default=0.8,
        help="Cooling factor (default: 0.8)"
    )
    parser.add_argument(
        "--eqc",
        type=float,
        default=1.0,
        help="Equilibrium coefficient (default: 1.0)"
    )

    args = parser.parse_args()

    return Input(
        file=args.file,
        solution=args.solution,
        it=args.it,
        et=args.et,
        cooling=args.cooling,
        eq_coefficient=args.eqc
    )

def main():
    try:
        # Parse input
        input_data = get_input()

        # Load instance file
        instance_path = Path("./Data") / input_data.file
        if not instance_path.is_file():
            raise FileNotFoundError(f"Unable to read instance file: {instance_path}")
        instance = Instance.parse(instance_path)

        # Load solution file
        solution_path = Path("./Data") / input_data.solution  # Adjusted for your file structure
        if not solution_path.is_file():
            raise FileNotFoundError(f"Unable to read solution file: {solution_path}")
        solutions = Solutions.parse(solution_path)
        solution = solutions.get(instance.name)

       

        # Initialize and run solver
        solver = Solver(
            instance,
            input_data.it,
            input_data.et,
            input_data.cooling,
            input_data.eq_coefficient
        )
        weight, final_state, iterations, rel_err, duration = solver.solve(solution)

        parent_folder_name = os.path.basename(os.path.dirname(input_data.file))
        results_file_path = Path("./Results") / f"res_{parent_folder_name}.csv"

        if not results_file_path.parent.exists():
            results_file_path.parent.mkdir(parents=True)

        # Save result to CSV
        with open(results_file_path, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow([instance.name, iterations, rel_err, duration, weight] + final_state) 

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
