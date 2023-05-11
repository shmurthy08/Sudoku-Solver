class Cell:
    def __init__(self, row: int, col: int, val: int, n: int) -> None:
        self.row = int(row)  # Row index of the cell
        self.col = int(col)  # Column index of the cell

        # Check if the row and column indices are within the valid range [0, n-1]
        if self.row >= n or self.col >= n:
            raise ValueError("Row and Column need to be in range [0,%s] inclusive" % (n - 1))

        self._val = int(val)  # Value of the cell
        self.is_modifiable = (self._val == 0)  # Indicates if the cell is modifiable

        # Check if the board dimension is a perfect square
        if n ** 0.5 == int(n ** 0.5):
            self.n = n  # Dimension of the board
            self.poss_vals = set(range(1, n + 1))  # Set of possible values for the cell
        else:
            raise ValueError("Invalid nxn board Dimension")

        # If the cell is not modifiable (contains a fixed value), clear the set of possible values
        if not self.is_modifiable:
            self.poss_vals = set()

    def getVal(self) -> int:
        return self._val

    def setVal(self, value: int) -> None:
        if self.is_modifiable: # Not a preset cell part of the base board
            self._val = value
            if len(self.poss_vals) == 1: # guaranteed cell
                self.poss_vals.clear()
        else:
            raise AttributeError("ERROR: Value is not writeable")
        return self.is_modifiable

    def remove_possibility(self, val: int) -> bool:
        # Remove a value from the set of possible values for the cell
        if val in self.poss_vals:
            self.poss_vals.remove(val)
            return True
        return False

    def __str__(self) -> str:
        red = "\033[0;31m"  # ANSI escape code for red color
        highlight = '\x1b[1;33m' + '\x1b[7m'  # ANSI escape code for highlighted text
        reset = "\033[0m"  # ANSI escape code to reset text formatting

        if self._val == 0:
            return '•'  # Display an empty cell
        elif self.is_modifiable:
            return str(self._val)  # Display the value of a modifiable cell
        else:
            return red + str(self._val) + reset  # Display the value of a non-modifiable cell in red


        # This will display additional information about the cell, including its possible values
        # if you are using this class to develop your own Sudoku Solver(s).
        # For debugging purposes, you can uncomment the following line
        
        # return """\"val:%s, r:%s, c:%s%s\"""" % ((('' if self._val != 0 else highlight) if self.is_modifiable else red) + str(self._val) + reset, self.row, self.col, "\n" + str(self.poss_vals) if len(self.poss_vals) != 0 else "")

    def __repr__(self) -> str:
        return str(self)
