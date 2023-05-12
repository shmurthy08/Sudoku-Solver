
# Sudoku-Solver
Hi, this is our CPSC 406, Algorithm Analysis, class project. The project members include Shree Murthy (me), Rahul Sura and Dylan Inafuku. Our goal is to create a sudoku solver with two types of solving methods to learn more about algorithms. See the link to our [presentation](https://docs.google.com/presentation/d/1JnC8Kd4kijPLFjV1sCchN6WeVRiDiY6CYxrkNO_E51w/edit#slide=id.g24023e6062c_1_33267)

## Personal Information:
- Shree Murthy: shmurthy@chapman.edu
- Rahul Sura: sura@chapman.edu
- Dylan Inafuku: dinafuku@chapman.edu
- Class: CPSC 406 - 02
- Instructor: Alexander Kurz
- Institution: Chapman University

## Introduction: 
Sudoku is a widely played puzzle game and we learned about it during our class discussions regarding the NP-Complete problem family discussed in class, including SAT-solvers. We sought to create a program that aims to be a companion for beginners. Essentially, the goal was that if a user gave a board that they are currently working on they can see how their solution matches up with the solutions of our methods. Furthermore, we wanted to explore how we can take the human thought process of solving sudoku and use code as a way to output that thought process. 

## Literature Review:
### [Literature Review #1](http://www.diva-portal.org/smash/get/diva2:811020/FULLTEXT01.pdf):
In this literature review, an algorithm analysis was conducted on two Sudoku solver algorithms, which are the pencil-and-paper method and the brute force method. The pencil-and-paper method is essentially a backtracking algorithm, similar to the backtracking approach used in our human solver algorithm. The brute force method is an algorithm that tries all possible combinations. Based on their tests and the results they gathered, the pencil-and-paper method greatly outperformed the brute force method. As the board increases in difficulty, the number of possible combinations of values also increases. Therefore, as the Sudoku board difficulty increases, so does the brute force algorithms' runtime, since it has a much larger number of possible combinations of values to test. The brute force method and pencil-and-paper methods were pretty close in terms of runtime for easy and medium difficulty boards, however, the brute force method performed exponentially worse for hard and extreme boards.

### [Literature Review #2](https://www.csc.kth.se/utbildning/kth/kurser/DD143X/dkand13/Group1Vahid/report/Aref-Fiorella-KexJobb-sist.pdf):
Two college students conducted a complexity/algorithm analysis on several Sudoku solving algorithms and compared them to one another. The three algorithms that they tested consisted of the backtracking algorithm, rule based algorithm, and the constraint algorithm. The backtracking algorithm is similar to our human method algorithm as our human method uses a form of backtracking to emulate a human thought process. The rule based algorithm implements a collection of different solver methods and uses them in conjunction. Finally, the constraint algorithm is similar to our logic programming method since it uses logic programming to outline the definitions and rules of Sudoku to reach a solution. In this literature review, the students presented their results in the form of a graph comparing each of the three solvers to their respective runtime for all board difficulties. Based on their testing, backtracking was the most efficient algorithm, rule based was a little less efficient than backtracking, and the constraint algorithm was the least efficient and had the longest runtime. After we completed our algorithms and conducted algorithm analysis, our results in terms of runtime matched that of this literature review's results. Our logic programming algorithm noticeably took the longest in terms of runtime for the sudoku boards, and our human method was the most efficient in terms of runtime, which is the same as the results that the college students gathered.

### Timeline:
- Brainstorming (weeks 1-3): Discussion of Board Generator finding articles for literature review
- Initial Development (weeks 4-6): Building solvers for 4x4 sudoku board
- Scaling (weeks 7-10): Scaling the solvers to solve 9x9 sudoku boards
- Post-Production (weeks 11-14): Developing a GUI to display boards and creating presentation

### To run the gui:
(Note, on windows use the `python` command and on linux, `python3`)
- `python sudoku_gui.py [SUDOKU_FILE]`
- To run with sample boards, click the `Generate Board` button. It will write over 
`sudoku_board.txt`

### Non-builtin python library dependencies:
- tabulate (`pip install tabulate`)
- pulp (`pip install pulp`)
- pygame (`pip install pygame`)
- requests (`pip install requests`)

### Documentation:
- Program was developed using python and the dependencies listed the previous section
- A [sudoku api](https://sudoku-api.vercel.app/) was used to create an unlimited number of sudoku boards of varying difficulties
- Components:
	- There are **two sudoku solvers** (solver_method_1.py and solver_method_2.py). Method 1 represents the human solver method (taking the human thought process and making it into code). Method 2 represents the computer method because Logic Programming takes all rules and throws them into a box to test and find how to solve the problem, so the user doesn’t know what the thought process of the computer is. 
	- One cell class: this interacts with solver_method_1.py to keep track of all cells that method 1 is trying to solve. 
	- Generator.py: this is used to call the sudoku api and generate a brand new board that can be used by the program
    - There is a GUI component that interacts with the two solver methods to beautifully output the solutions to the PyGame GUI window. Also interacts with Generator.py to generate brand new boards that can be solved.
	


### Data Structures and Algorithms:
- solver_method_1.py:
```

Data Structures:

- 2D List (Grid): It represents the Sudoku grid, where each cell is an instance of the Cell class. The grid is used to store and manipulate the Sudoku puzzle.

Algorithms:

- Backtracking Algorithm: The solve method implements a backtracking algorithm to solve the Sudoku puzzle. It systematically explores all possible solutions by making choices and undoing them if they lead to invalid states. The backtracking algorithm is used to find the solution recursively.

- Constraint Propagation: The remove_possibilities method is responsible for removing possibilities for unfilled cells based on the values filled in other cells. It propagates constraints by eliminating possible values for cells in the same row, column, and 3x3 sub-grid when a value is assigned to a cell.

- Unassigned Location Finding: The find_unassigned_location method is used to find the next unassigned location (empty cell) in the grid. It iterates through the grid and returns the coordinates of the first empty cell it encounters.

- Safe Placement Check: The is_safe method checks if it is safe to place a number in a specific cell. It verifies if the number violates any Sudoku rules in the same row, column, or 3x3 sub-grid.

Conclusion: These data structures and algorithms work together to solve the Sudoku puzzle by exploring the solution space, making informed choices, and backtracking when necessary.
```
- solver_method_2.py
```
Data Structures:

- 2D List (self.board): It represents the initial Sudoku board read from a file. Each cell of the board is stored as a character in a 2D list.

Algorithms:

- Integer Linear Programming (ILP): The solve_puzzle method formulates the Sudoku puzzle as an ILP problem using the PuLP library. It sets up decision variables (choices) as binary variables representing whether a number is chosen for a particular cell. It defines constraints to ensure that each cell, row, column, and sub-grid contains exactly one number from 1 to 9. The ILP solver is then used to find the optimal solution. The ILP approach is different from the backtracking algorithm used in SudokuSolver1. It formulates the Sudoku puzzle as a mathematical optimization problem and uses the ILP solver to find the solution by optimizing the objective function (which is set to a constant value in this case).

Conclusion: Overall, the SudokuSolver2 class uses ILP and a different modeling approach to find the solution to the Sudoku puzzle. It relies on the PuLP library and the mathematical optimization capabilities provided by the ILP solver.
```

- cell.py: this file doesn’t contain any popular algorithms and doesn’t use a lot of data structures (everything is done using a set) however we will analyze everything within the code for a comprehensive review:

```
Data Structures:

Instance Variables: row, col, _val, is_modifiable, n, poss_vals
- row (int): Row index of the cell.
- col (int): Column index of the cell.
- _val (int): Value of the cell.
- is_modifiable (bool): Indicates if the cell is modifiable (contains a fixed value).
- n (int): Dimension of the board.
- poss_vals (set): Set of possible values for the cell.

Algorithms:

- __init__(self, row: int, col: int, val: int, n: int) -> None: Performs validation checks on the input values, such as the row and column indices, board dimension, and modifiability of the cell. However, it does not involve any significant algorithmic operations.

- getVal(self) -> int: Simply returns the value of the cell without performing any complex computations.

- setVal(self, value: int) -> None: Sets the value of the cell if it is modifiable, but it does not involve any complex algorithms.

- remove_possibility(self, val: int) -> bool: Removes a value from the set of possible values for the cell, which is a basic set operation rather than an algorithmic process.

- __str__(self) -> str: Generates a string representation of the cell based on its value and modifiability. It does not involve any complex algorithms.

- __repr__(self) -> str: Generates a string representation of the cell without any involved algorithms.


Conclusion: In summary, the Cell class mainly implements data structures, such as instance variables and sets, to represent and manage the properties of a Sudoku cell. The class does not utilize complex algorithms but rather provides basic functionality to access, modify, and display cell information.


```

### Changes to plans?
- We didn’t have any changes to the plan that swayed us to adjust our entire project
- Everything in the Timeline was achieved and there weren’t any large adjustments made, other than needing to account for multiple solutions
- There is nothing left to do, future groups can reference our **Future Developments** section to find out what to do next

### Future development
- Have a runtime complexity analysis on the statistics page for every difficulty for multiple iterations
```
Example Stats:

Easy Avg:
	Human:	0.0000002 sec
	LP:		0.003 sec

Medium Avg:
	Human:	0.000003 sec
	LP:		0.005 sec

Hard Avg:
	Human:	0.008 sec
	LP:		0.006 sec

Extreme Avg:
	Human:	2.712 sec
	LP:		0.012 sec

```
- Include file uploading for board file as a GUI function and adding user input for board values instead of uploading a custom formatted file
- Implement other sudoku algorithms like naked single and others to see how it will compete with existing algorithms. 

### What worked and what didn’t work
- During the early parts of the project “solver_method_1.py” wasn’t working for sudoku boards that had more than one solution and only worked for boards that had one specific solutions
- At the end of the project everything we set out to achieve was completed in a timely manner and everything works as intended. 

### Results and Achievements:
- Human Solver outperformed the Logic Programming solver (most of the time)
- For some of the more complicated puzzles (like ‘extreme’), Human Solver was significantly slower. Logic programming is more consistent in terms of how long it takes to solve (less variability in number of seconds)
- In line with literature review results

### Testing methods
- Sudoku is a puzzle that really only has a few rules for the puzzle to be fully solved. Hence, other than using a Sudoku board validator that takes those rules into account, there isn’t any other way to perform a test that both methods are working correctly, just that the end result is correct or incorrect.
- It's also important to note that if you feed in an invalid Sudoku base text file that already violates the constraints of Sudoku (like two of the same number in the same row), the two solvers will still try its best to solve the board to the best of its ability, but since there is no way to fully solve it, the filled in numbers will not be accurate. Of course, we would hope that people would use the program to actually solve a board and not to break it.
- Also, to test the programs themselves to see which is better, the best thing we thought of was to use Python’s time package to figure out how long the program takes to run. We also compared the runtime efficiencies to determine which method generally outperforms the other at each board difficulty level (easy, medium, hard, extreme).
- We initially tested both methods using a 4x4 board and then scaled up the solution to work for 9x9. We also tried boards with guaranteed only one solution and ones with multiple solutions to periodically make sure that the code still works for only one solution and for multiple solutions as well. If you would like to see the file we used to test the boards for 4x4, you can run `method_testing_4x4.py` with `example_4x4_grid.txt`.
- If there are other ways to test please inform us via a Git Issue, pull request, or by any other means.

### Work Divided:

- Shree: Coded Logic Programming Solver
- Rahul: Coded Human solver
- Dylan: Coded GUI and used Sudoku API to generate boards

- All group members helped each other figure out bug issues as well as help when others were stuck. All members helped analyze literature review studies



### Helpful Links:
- [Learn about PuLP package](https://data-flair.training/blogs/python-logic-programming/)
- [PuLP Documentation](https://coin-or.github.io/pulp/)
- [Literature Review #1](http://www.diva-portal.org/smash/get/diva2:811020/FULLTEXT01.pdf)
- [Literature Review #2](https://www.csc.kth.se/utbildning/kth/kurser/DD143X/dkand13/Group1Vahid/report/Aref-Fiorella-KexJobb-sist.pdf)
