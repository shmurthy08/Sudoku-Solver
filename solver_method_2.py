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
        choices = LpVariable.dicts("Choice", (range(9), range(9), range(1, 10)), cat='Binary')

        # Set the objective function to a constant value
        prob += 0

        # Define constraints
        # Each cell should be filled with a number from 1 to 9
        for i in range(9):
            for j in range(9):
                prob += lpSum([choices[i][j][k] for k in range(1, 10)]) == 1

        # Each row should contain all numbers from 1 to 9 exactly once
        for i in range(9):
            for k in range(1, 10):
                prob += lpSum([choices[i][j][k] for j in range(9)]) == 1

        # Each column should contain all numbers from 1 to 9 exactly once
        for j in range(9):
            for k in range(1, 10):
                prob += lpSum([choices[i][j][k] for i in range(9)]) == 1

        # Each 3x3 sub-grid should contain all numbers from 1 to 9 exactly once
        for x in range(3):
            for y in range(3):
                for k in range(1, 10):
                    prob += lpSum([choices[i][j][k] for i in range(3*x, 3*x+3) for j in range(3*y, 3*y+3)]) == 1

        # Set the initial values of the cells that you read from the file
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != '.':
                    k = int(self.board[i][j])
                    prob += choices[i][j][k] == 1

        LpSolverDefault.msg = 0
        # Solve the problem
        prob.solve()

        # LpSolverDefault.msg = 1

        # Extract the solution from the variables
        solution = np.zeros((9, 9), dtype=int)
        for i in range(9):
            for j in range(9):
                for k in range(1, 10):
                    if value(choices[i][j][k]) == 1:
                        solution[i][j] = k

        # Print the solution
        # print(solution)
        return solution