import numpy as np
import time
import random
import math
import matplotlib.pyplot as plt
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
        self.prices = []  # List to store price values during iterations
        self.total_clauses = len(self.instance.clauses)

        
    
    def solve(self, solution):
        start = time.time()
        weight, final_state = self.run()
        end = time.time()
        duration = (end - start) * 1e6 
        expected_weighted_sum = solution['weight']
        rel_err = self.calc_rel_err(weight, expected_weighted_sum)
        format_time = str(f"{int(duration)}\u00b5s")
        unformat_time=str(f"{int(duration)}")
        format_rel_err = str(f"{rel_err:.2f}%")
        unformat_rel_err = str(f"{rel_err:.2f}").replace('.', ',')
        print(f"#iterations:{self.iter_num}  rel err:{format_rel_err}  time:{format_time} expected: {expected_weighted_sum} got: {weight} solved: {self.is_valid(final_state)} ")
        self.plot_price(expected_weighted_sum)  # Plot price after the algorithm finishes
        return weight, self.iter_num, unformat_rel_err, unformat_time
    
    @staticmethod
    def calc_rel_err(actual, expected):
        return abs(expected - actual) * 100.0 if expected == 0 else abs(expected - actual) / expected * 100.0
    
    def run(self):
        temp = self.create_init_state()
       
        if self.is_valid(temp):
            best_state = temp 
            curr_state = best_state[:] 
            best_price = self.calc_price(best_state) 
            curr_price = best_price
        else:
            best_state = np.zeros(self.instance.n, dtype=bool)
            curr_state = temp    
            best_price = 0
            curr_price = self.calc_price(curr_state)     
        t = self.init_temp * self.instance.n
        print(f"pocatecni teplota: {t}")
        found_valid_state = False

        while t >= self.freeze*self.instance.n: 
            for _ in range(self.equilibrium): 
                curr_state = self.new_state(curr_state, curr_price, t) 
                curr_price = self.calc_price(curr_state)
                valid = self.is_valid(curr_state)
                
                if valid:
                    found_valid_state = True
                if valid and curr_price > best_price: 
                    best_price = curr_price 
                    best_state = curr_state.copy() 
                self.prices.append(curr_price)     
                self.iter_num += 1 
            t *= self.cooling  # Decrease temperature for the next iteration

        if not found_valid_state:
            print(f"No valid state found during the cooling process.")
        return best_price, best_state if found_valid_state else curr_state 
    
    def create_init_state(self):
        return self.rand_state()
    
    def new_state(self, state, price, t):
        new_state = self.better_change_state(state)
        new_price = self.calc_price(new_state) 
        sat_new = self.calc_satisfied_clauses(new_state)
        sat_old = self.calc_satisfied_clauses(state)
  
        delta = (new_price * sat_new / self.total_clauses) - (price * sat_old / self.total_clauses) 
        if delta > 0:
            return new_state 
        
        choice = self.rng.uniform(0, 1) 
        if choice < math.exp(-abs(delta) / t):
            return new_state 
        return state.copy()

    def better_change_state(self, state):
        new_state = state.copy()
        # Decide whether to flip randomly (10%) or unsatisfied literals (90%)
        if self.rng.uniform(0, 1) < 0.10:  # 10% chance for random flip of 3-5 variables
            num_flips = self.rng.randint(3, 5)  # Flip between 3 and 5 variables
            num_flips = min(num_flips, self.instance.n)  # Ensure we do not exceed the number of variables
            indices = np.random.choice(self.instance.n, num_flips, replace=False)
            new_state[indices] = ~new_state[indices]  # Flip the chosen indices
        else:
            # 90% chance to flip one of the unsatisfied clause literals
            unsatisfied_clauses = [
                clause for clause in self.instance.clauses if not clause.eval(state)
            ]

            if unsatisfied_clauses:  # If there are unsatisfied clauses
                clause_to_flip = self.rng.choice(unsatisfied_clauses)  # Choose a random unsatisfied clause
                literal_to_flip = self.rng.choice(clause_to_flip.literals)  # Random literal in the chosen clause
                var_index = literal_to_flip.get_id() - 1  # Get the variable index (1-based to 0-based)
                new_state[var_index] = not new_state[var_index]  # Flip the literal in the state
        return new_state 
    
    def rand_state(self):
        return np.random.choice([True, False], size=self.instance.n)
    
    def calc_satisfied_clauses(self, state):
        return sum(
            any(state[abs(lit.get_id()) - 1] == (not lit.is_neg) for lit in clause.literals)
            for clause in self.instance.clauses
        )
    
    def calc_price(self, state):
        return np.sum(self.instance.weights[state])  # Optimized with numpy
    
    def is_valid(self, state):
        return all(clause.eval(state) for clause in self.instance.clauses)
    
    def plot_price(self, expected_weighted_sum):
        """Plot the price over iterations."""
        plt.figure(figsize=(10, 6))
        plt.plot(self.prices, label="Aktuální cena")
        plt.axhline(y=expected_weighted_sum, color='r', linestyle='--', label="Optimální cena")
        plt.xlabel("Kroky")
        plt.ylabel("Cena")
        plt.title("Simulované chlazení: aktuální cena/kroky")
        plt.legend()
        plt.grid()
        plt.savefig("price_plot.png")  # Save the plot as a PNG
        plt.close()
