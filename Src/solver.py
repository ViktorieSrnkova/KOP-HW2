import time
import random
import math
from pathlib import Path
from parser import Instance, Solutions
class Solver:
    
    def __init__(self, instance, it, et, cooling, eq_coefficient):
        self.instance = instance
        self.rng = random.Random()
        self.iter_num = 0
        self.cooling = cooling
        self.init_temp = float(it)
        self.freeze = float(et)
        self.equilibrium = int(self.instance.n * eq_coefficient)
    
    def solve(self, solution):
        start = time.time()
        weight,final_state= self.run()
        end = time.time()
        duration = (end - start) * 1e6 
        #formatted_state = [(i + 1) if val else -(i + 1) for i, val in enumerate(final_state)]
        expected_weighted_sum =solution['weight']
        rel_err = self.calc_rel_err(weight, expected_weighted_sum)
        format_time=str(f"{int(duration)}\u00b5s")
        format_rel_err=str(f"{rel_err:.2f}%")
        unformat_rel_err=str(f"{rel_err:.2f}")
        print(f"#iterations:{self.iter_num}  rel err:{format_rel_err}  time:{format_time} expected: {expected_weighted_sum} got: {weight} solved: {self.is_valid(final_state)} ")
        return  weight, final_state, self.iter_num, unformat_rel_err, format_time
    
    @staticmethod
    def calc_rel_err(actual, expected):
        return abs(expected - actual) * 100.0 if expected == 0 else abs(expected - actual)/expected *100.0
    
    def run(self):
        temp = self.create_init_state()
       
        if self.is_valid(temp):
            best_state = temp 
            curr_state = best_state[:] 
            best_price = self.calc_price(best_state) 
            curr_price = best_price
        else:
            best_state = []
            curr_state = temp    
            best_price = 0
            curr_price = self.calc_price(curr_state)     
        t = self.init_temp
        found_valid_state = False
        while t >= self.freeze: 
            for _ in range(self.equilibrium): 
                curr_state = self.new_state(curr_state, curr_price, t) 
                curr_price = self.calc_price(curr_state)
                valid = self.is_valid(curr_state)
                if valid:
                    found_valid_state = True
                if valid and curr_price > best_price: 
                    best_price = curr_price 
                    best_state = curr_state[:] 
                self.iter_num += 1 
            t *= self.cooling 

        if not found_valid_state:
            print(f"No valid state found during the cooling process.")
    
        return best_price, best_state if found_valid_state else curr_state 
    
    def create_init_state(self):
        return [True] * self.instance.n

        return self.rand_state()
    
    def new_state(self, state, price, t):
        new_state = self.better_change_state(state)
        new_price = self.calc_price(new_state) 
        if new_price > price: 
            return new_state 
        delta = price - new_price 
        choice = self.rng.uniform(0, 1) 
        if choice < math.exp(-delta / t):
            return new_state 
        return state[:] 
    

    def better_change_state(self, state):
        new_state = state[:]
        vars = [lit.get_id() for clause in self.instance.clauses if not clause.eval(new_state) for lit in clause.literals] 
        if not vars: 
            return state[:] 
        index = self.rand_uint(0, len(vars) - 1) 
        new_state[vars[index] - 1] = not new_state[vars[index] - 1]
        return new_state 
    
    def rand_state(self):
        return [self.rng.choice([True, False]) for _ in range(self.instance.n)] 
    
    def calc_price(self, state):
        return sum(weight for is_true, weight in zip(state, self.instance.weights) if is_true)  
    
    def is_valid(self, state):
        return all(clause.eval(state) for clause in self.instance.clauses)
    
    def rand_uint(self, from_, to):
        return self.rng.randint(from_, to) 
    
    @staticmethod
    def load_instance(file_path):
        instance_path = Path("Data") / file_path
        if not instance_path.is_file():
            raise FileNotFoundError(f"Unable to read instance file: {instance_path}")
        return Instance.parse(instance_path)
    
    @staticmethod
    def load_solution(file_path):
        solution_path = Path("Data") / file_path
        if not solution_path.is_file():
            raise FileNotFoundError(f"Unable to read solution file: {solution_path}")
        solutions = Solutions.parse(solution_path)
        return solutions