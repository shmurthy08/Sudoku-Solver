from cell import Cell
from typing import *
import tabulate
import sys

Grid = List[List[Cell]]

def print_grid(grid: Grid) -> None:
    print(tabulate.tabulate(grid, tablefmt="grid"))

def read_file(file_name: str) -> Grid:
    try:
        file = open(file_name)
    except:
        raise FileNotFoundError("ERROR: File not found")
    
    lines = [line.strip() for line in file.readlines()]
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
                remove_possibilities(grid, row_index, col_index, val.getVal())
    
    return grid

def remove_possibilities(grid: Grid, row: int, col: int, value: int) -> None:
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

def solve(grid: Grid) -> None:
    all_cells = [cell for cell_row in grid for cell in cell_row]
    all_cells.sort(key=lambda c: len(c.poss_vals))
    while len(all_cells) > 0:
        all_cells.sort(key=lambda c: len(c.poss_vals))
        while len(all_cells) > 0 and len(all_cells[0].poss_vals) == 0:
            all_cells.pop(0)
        if len(all_cells) > 0 and len(all_cells[0].poss_vals) == 1:
            value = all_cells[0].poss_vals.pop()
            all_cells[0].setVal(value)
            all_cells[0].remove_possibility(value)
            remove_possibilities(grid, all_cells[0].row, all_cells[0].col,all_cells[0].getVal())
            all_cells.pop(0)
        else:
            print("ERROR: No unique solution") # Still needs to be implemented if there are multiple solutions

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("ERROR: No specified file to solve. Add it in the command line arguments")
        exit()
    try:
        grid = read_file(sys.argv[1])
    except:
        print("ERROR: Invalid file")
        exit()
    print("Unsolved Grid: (Red indicates the originally provided numbers)")
    print_grid(grid)
    print("Solved Grid: (Red indicates the originally provided numbers)")
    solve(grid)
    print_grid(grid)