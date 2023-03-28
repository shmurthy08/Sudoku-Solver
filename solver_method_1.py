from cell import Cell
from typing import *
import tabulate
import sys

Grid = List[List[Cell]]

def print_grid(grid: Grid) -> None:
    print(tabulate.tabulate(grid, tablefmt="grid"))