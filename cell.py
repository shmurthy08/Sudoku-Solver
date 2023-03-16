class Cell:
    def __init__(self, row: int, col: int, val: int, n: int) -> None:
        self.row = int(row)
        self.col = int(col)
        if self.row >= n or self.col >= n:
            raise ValueError("Row and Column need to be in range [0,%s] inclusive" % (n-1))
        self._val = int(val)
        self.is_modifiable = (self._val == 0)
        
        if n ** 0.5 == int(n ** 0.5):
            self.n = n
            self.poss_vals = set(range(1,n + 1))
        else:
            raise ValueError("Invalid nxn board Dimension")
        
        if not self.is_modifiable:
            self.poss_vals = set()

    def getVal(self) -> int:
        return self._val
    
    def setVal(self, value) -> None:
        if self.is_modifiable:
            self._val = value
            if len(self.poss_vals) == 1:
                self.poss_vals.clear()
        else:
            raise AttributeError("ERROR: Value is not writeable")
        return self.is_modifiable

    def remove_possibility(self, val: int) -> bool:
        if val in self.poss_vals:
            self.poss_vals.remove(val)
            return True
        return False

    def __str__(self) -> str:
        red = "\033[0;31m"
        reset = "\033[0m"
        if self._val == 0:
            return '•'
        elif self.is_modifiable:
            return str(self._val)
        else:
            return red + str(self._val) + reset
        
        # For debugging:
        
        # return """\"val:%s, r:%s, c:%s%s\"""" % (red + str(self._val) + reset, self.row, self.col, ", " + str(self.poss_vals) if len(self.poss_vals) != 0 else "")
    
    def __repr__(self) -> str:
        return str(self)