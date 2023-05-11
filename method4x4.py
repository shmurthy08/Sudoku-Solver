import numpy as np
from pulp import *


class SudokuSolver2:
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
