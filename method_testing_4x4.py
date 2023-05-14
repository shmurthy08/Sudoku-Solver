import numpy as np
from time import time
from pulp import *
from solver_method_1 import SudokuSolver1
from tabulate import tabulate

class SudokuSolver2_4x4:
    def __init__(self, filename):
        # Read the initial board from file
        self.board = []
        with open(filename, 'r') as f:
            lines = f.readlines()
            for i in range(0, len(lines)):
                row = list(lines[i].strip())
                self.board.append(row)

    def solve_puzzle(self):
        # Initialize the problem
        prob = LpProblem("SudokuSolver", LpMinimize)

        # Define the variables
        choices = LpVariable.dicts("Choice", (range(4), range(4), range(1, 5)), cat='Binary')

        # Set the objective function to a constant value
        prob += 0

        # Define constraints
        # Each cell should be filled with a number from 1 to 4
        for i in range(4):
            for j in range(4):
                prob += lpSum([choices[i][j][k] for k in range(1, 5)]) == 1

        # Each row should contain all numbers from 1 to 4 exactly once
        for i in range(4):
            for k in range(1, 5):
                prob += lpSum([choices[i][j][k] for j in range(4)]) == 1

        # Each column should contain all numbers from 1 to 4 exactly once
        for j in range(4):
            for k in range(1, 5):
                prob += lpSum([choices[i][j][k] for i in range(4)]) == 1

        # Each 2x2 sub-grid should contain all numbers from 1 to 4 exactly once
        for x in range(2):
            for y in range(2):
                for k in range(1, 5):
                    prob += lpSum([choices[i][j][k] for i in range(2*x, 2*x+2) for j in range(2*y, 2*y+2)]) == 1

        # Set the initial values of the cells that you read from the file
        for i in range(4):
            for j in range(4):
                if self.board[i][j] != '.':
                    k = int(self.board[i][j])
                    prob += choices[i][j][k] == 1

        # Doesn't output any information to terminal because everything is visible in the GUI
        LpSolverDefault.msg = 0
        # Solve the problem
        prob.solve()

        # Extract the solution from the variables
        solution = np.zeros((4, 4), dtype=int)
        for i in range(4):
            for j in range(4):
                for k in range(1, 5):
                    if value(choices[i][j][k]) == 1:
                        solution[i][j] = k

        # Print the solution
        return solution


# main just for testing 4x4
if __name__ == '__main__':
    if len(sys.argv) < 2: # command line argument for file
        print("ERROR: No specified file to solve. Add it in the command line arguments")
        exit()
    solver1 = SudokuSolver1(sys.argv[1])
    
    # Print method 1
    print("Method 1 (Backtracking)")
    print("Unsolved Grid: (Red indicates the originally provided numbers)")
    print(tabulate(solver1.grid, tablefmt='grid'))
    print("Solved Grid: (Red indicates the originally provided numbers)")
    sovler1_start_time = time()
    if solver1.solve(solver1.grid): # if there is a solution
        sovler1_end_time = time()
        print(tabulate(solver1.grid, tablefmt='grid')) # print the solution
        print(f"Took {sovler1_end_time - sovler1_start_time} seconds to solve")
    else:
        print("No solution")
    
    # Print method 2
    solver2 = SudokuSolver2_4x4(sys.argv[1])
    print("Method 2 (Logic Programming) solution")
    sovler2_start_time = time()
    end_soln = solver2.solve_puzzle()
    sovler2_end_time = time()
    print(tabulate(end_soln, tablefmt='grid'))
    print(f"Took {sovler2_end_time - sovler2_start_time} seconds to solve")