from cell import Cell
from typing import *

Grid = List[List[Cell]]

class SudokuSolver1:
    def __init__(self, filename: str):
        # initalize number of stack calls to zero
        self.num_stack_calls = 0
        # initialize the grid of cells
        self.grid = self.read_file(filename)

    def read_file(self, file_name: str) -> Grid:
        try:
            file = open(file_name)
        except:
            raise FileNotFoundError("ERROR: File not found")
        
        # get the lines from the file
        lines = [line.strip() for line in file.readlines() if line.strip() != '']
        grid: Grid
        grid = []
        n = len(lines[0]) # 4x4 or 9x9 grid
        
        # fill in the board with the necessary values
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
        
        # remove the possibilities for the unfilled cells
        for row_index, row in enumerate(grid):
            for col_index, val in enumerate(row):
                if grid[row_index][col_index].getVal() != 0:
                    self.remove_possibilities(grid, row_index, col_index, val.getVal())
        
        return grid

    def remove_possibilities(self, grid: Grid, row: int, col: int, value: int) -> None:
        self.num_stack_calls += 1
        n = grid[row][col].n
        sqrt = int(n ** 0.5)
        
        # remove the possibility for every cell in the same row and column
        for i in range(n):
            grid[row][i].remove_possibility(value)
            grid[i][col].remove_possibility(value)
        
        start_row = (row // sqrt) * sqrt
        start_col = (col // sqrt) * sqrt
        
        # remove the possibility for every cell in the same sub-square (3x3)
        for i in range(start_row, start_row + sqrt):
            for j in range(start_col, start_col + sqrt):
                grid[i][j].remove_possibility(value)

    def find_unassigned_location(self, grid: Grid) -> Tuple[int, int]:
        self.num_stack_calls += 1
        
        cell_row, cell_col = -1, -1
        # find first empty cell to compare min possibilities to
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col].getVal() == 0:
                    cell_row, cell_col = row, col
        
        #fully filled
        if cell_row == -1 and cell_col == -1:
            return cell_row, cell_col
        
        # find where the cell's value is 0
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                curr_cell = grid[row][col]
                if curr_cell.getVal() == 0: # empty cell
                    if len(curr_cell.poss_vals) == 1: # guaranteed only one value
                        guaranteed_val = curr_cell.poss_vals.pop()
                        self.remove_possibilities(grid, row, col, guaranteed_val)
                        curr_cell.poss_vals.add(guaranteed_val)
                        return row, col
                    elif len(curr_cell.poss_vals) < len(grid[cell_row][cell_col].poss_vals):
                        # otherwise, has less possibilities
                        cell_row, cell_col = row, col
        
        # all cells are filled in
        return cell_row, cell_col

    def is_safe(self, grid: Grid, row: int, col: int, num: int) -> bool:
        self.num_stack_calls += 1
        
        # if value in the same row
        if num in [grid[row][i].getVal() for i in range(len(grid))]:
            return False

        # if value in the same col
        if num in [grid[i][col].getVal() for i in range(len(grid))]:
            return False

        sqrt = int(len(grid) ** 0.5)
        box_row = row // sqrt
        box_col = col // sqrt

        # if value in the same sub_square
        for i in range(box_row * sqrt, box_row * sqrt + sqrt):
            for j in range(box_col * sqrt, box_col * sqrt + sqrt):
                if grid[i][j].getVal() == num:
                    return False
        return True

    def solve(self, grid: Grid) -> bool:
        self.num_stack_calls += 1
        
        # find first empty cell
        row, col = self.find_unassigned_location(grid)

        # solved the grid. accessible via self.grid from external python files
        if row == -1 and col == -1:
            return True

        # iterates from 1-9
        for num in range(1, len(grid) + 1):
            
            # if num is a possible value
            if self.is_safe(grid, row, col, num):
                
                grid[row][col].setVal(num) # temporarily set the value
                if self.solve(grid): # recursively solve and if it works, return True
                    return True
                grid[row][col].setVal(0) # otherwise, reset the value and try again

        return False

