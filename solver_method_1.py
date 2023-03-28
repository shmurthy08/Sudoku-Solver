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
    ...