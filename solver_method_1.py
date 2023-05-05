from cell import Cell
from typing import *
import sys
import time

Grid = List[List[Cell]]

class SudokuSolver1:
    def __init__(self, filename: str):
        self.num_stack_calls = 0
        self.grid = self.read_file(filename)
    
    def print_grid(self, grid: Grid) -> None:
        from tabulate import tabulate
        print(tabulate(grid, tablefmt="grid"))

    def read_file(self, file_name: str) -> Grid:
        try:
            file = open(file_name)
        except:
            raise FileNotFoundError("ERROR: File not found")
        
        lines = [line.strip() for line in file.readlines() if line.strip() != '']
        grid: Grid
        grid = []
        n = len(lines[0])
        for row, line in enumerate(lines):
            cell_row = []
            for col, val in enumerate(line):
                if val.isdigit():
                    val = int(val)
                    if val not in range(n + 1):
                        raise ValueError("Value of cell needs to be from [1,%s] inclusive or a 0 or '.' for an empty cell" % (n))
                    cell_row.append(Cell(row=row, col=col, val=int(val), n=n))
                else:
                    cell_row.append(Cell(row=row, col=col, val=0, n=n))
            grid.append(cell_row)
        
        for row_index, row in enumerate(grid):
            for col_index, val in enumerate(row):
                if grid[row_index][col_index].getVal() != 0:
                    self.remove_possibilities(grid, row_index, col_index, val.getVal())
        
        return grid

    def remove_possibilities(self, grid: Grid, row: int, col: int, value: int) -> None:
        self.num_stack_calls += 1
        n = grid[row][col].n
        sqrt = int(n ** 0.5)
        for i in range(n):
            grid[row][i].remove_possibility(value)
            grid[i][col].remove_possibility(value)
        
        start_row = (row // sqrt) * sqrt
        start_col = (col // sqrt) * sqrt
        for i in range(start_row, start_row + sqrt):
            for j in range(start_col, start_col + sqrt):
                grid[i][j].remove_possibility(value)

    def find_unassigned_location(self, grid: Grid) -> Tuple[int, int]:
        self.num_stack_calls += 1
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col].getVal() == 0:
                    return row, col
        return -1, -1

    def is_safe(self, grid: Grid, row: int, col: int, num: int) -> bool:
        self.num_stack_calls += 1
        if num in [grid[row][i].getVal() for i in range(len(grid))]:
            return False

        if num in [grid[i][col].getVal() for i in range(len(grid))]:
            return False

        sqrt = int(len(grid) ** 0.5)
        box_row = row // sqrt
        box_col = col // sqrt

        for i in range(box_row * sqrt, box_row * sqrt + sqrt):
            for j in range(box_col * sqrt, box_col * sqrt + sqrt):
                if grid[i][j].getVal() == num:
                    return False
        return True

    def solve(self, grid: Grid) -> bool:
        self.num_stack_calls += 1
        row, col = self.find_unassigned_location(grid)

        if row == -1 and col == -1:
            return True

        for num in range(1, len(grid) + 1):
            if self.is_safe(grid, row, col, num):
                grid[row][col].setVal(num)
                if self.solve(grid):
                    return True
                grid[row][col].setVal(0)

        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("ERROR: No specified file to solve. Add it in the command line arguments")
        exit()
    solver = SudokuSolver1(sys.argv[1])
    print("Unsolved Grid: (Red indicates the originally provided numbers)")
    solver.print_grid(solver.grid)
    print("Solved Grid: (Red indicates the originally provided numbers)")
    start_time = time.time()
    if solver.solve(solver.grid):
        end_time = time.time()
        solver.print_grid(solver.grid)
        print("Time it took to solve the board:", round(end_time - start_time, 2), "seconds")
    else:
        print("ERROR: No solution")
