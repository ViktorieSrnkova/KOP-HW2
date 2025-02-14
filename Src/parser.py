import re
from typing import List
import numpy as np
import os

class Instance:
    def __init__(self, name: str, n: int, weights: np.ndarray, clauses: List['Clause']):
        self.name = name
        self.n = n  # number of variables
        self.weights = weights  # Numpy array for weights
        self.clauses = clauses

    @staticmethod
    def parse(file_path: str) -> 'Instance':
        # Rozlišení složky na základě cesty
        folder_name = os.path.basename(os.path.dirname(os.path.dirname(file_path)))

        name, n, weights, clauses = "", 0, None, []
        with open(file_path, 'r') as f:
            for i, line in enumerate(f):
                line = line.strip()

                # Speciální případ pro složku 'wruf36-157'
                if folder_name == "wruf36-157R":
                    if i == 3:
                        name, n = Instance.parse_name_and_n_special(line)
                    elif i == 4:
                        weights = Instance.parse_weights(line, n)
                    elif line and i > 5:
                        clauses.append(Instance.parse_clause(line))
                else:
                    if i == 7:
                        name, n = Instance.parse_name_and_n(line)
                    elif i == 9:
                        weights = Instance.parse_weights(line, n)
                    elif line and i > 10:  # Start parsing clauses after line 10
                        clauses.append(Instance.parse_clause(line))

        return Instance(name, n, weights, clauses)

    @staticmethod
    def parse_name_and_n(line: str) -> tuple:
        # Regex to extract name (e.g., uf20-71)
        match_name = re.search(r"SAT instance\s+[\w/-]+/([\w-]+)", line)
        if match_name:
            name = match_name.group(1)
            # Extract the number (n) from the name
            match_n = re.search(r"f(\d+)-", name)
            if match_n:
                n = int(match_n.group(1))
                return name, n
            else:
                raise ValueError(f"Unrecognized format for number in name: {name}")
        else:
            raise ValueError(f"Unrecognized format for instance name: {line}")

    @staticmethod
    def parse_name_and_n_special(line: str) -> tuple:
        # Special parser for 'wruf36-157'
        match_name = re.search(r"c SAT instance .*/([\w-]+)", line)
        if match_name:
            name = match_name.group(1)
            # Extract the number (n) from the name
            match_n = re.search(r"ruf(\d+)-", name)
            if match_n:
                n = int(match_n.group(1))
                return name, n
            else:
                raise ValueError(f"Unrecognized format for number in name: {name}")
        else:
            raise ValueError(f"Unrecognized format for instance name: {line}")

    @staticmethod
    def parse_weights(line: str, n: int) -> np.ndarray:
        nums = line.strip().split()[1:]
        if len(nums) < n:
            print(f"Warning: Not enough weight values in line. Found {len(nums)}, expected {n}.")
        return np.array([int(weight_str) for weight_str in nums[:n]], dtype=np.int32)

    @staticmethod
    def parse_clause(line: str) -> 'Clause':
        # Split the line, convert to integers, and filter out zeros
        literals = [Literal(int(num)) for num in line.split() if num != '0']
        return Clause(literals)


class Clause:
    def __init__(self, literals: List['Literal']):
        self.literals = literals

    def eval(self, values: np.ndarray) -> bool:
        return any(lit.eval(values) for lit in self.literals)


class Literal:
    def __init__(self, id: int):
        self.id = abs(id)
        self.is_neg = id < 0

    def eval(self, values: np.ndarray) -> bool:
        value = values[self.id - 1]
        return not value if self.is_neg else value

    def get_id(self) -> int:
        return self.id
    
class Solutions:
    @staticmethod
    def parse(file_path):
        solutions = {}
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                instance_name = parts[0]
                weight = int(parts[1])
                solution = list(map(int, parts[2:-1]))  # Exclude the first two numbers and the last zero
                solutions[instance_name] = {'solution': solution, 'weight': weight}
        return solutions
