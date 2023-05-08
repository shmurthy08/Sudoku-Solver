# Sudoku-Solver
Hi, this is our CPSC 406, Algorithm Analysis, class project. The project members include Shree Murthy (me), Rahul Sura and Dylan Inafuku. Our goal is to create a sudoku solver with two types of solving methods to learn more about algorithms. See the link to our presentation [here](https://docs.google.com/presentation/d/1JnC8Kd4kijPLFjV1sCchN6WeVRiDiY6CYxrkNO_E51w/edit#slide=id.g24023e6062c_1_33267)

Non-builtin python library dependencies:
- tabulate (`pip install tabulate`)
- pulp (`pip install pulp`)
- pygame (`pip install pygame`)
- requests (`pip install requests`)

To run the gui:
(Note, on windows use the `python` command and on linux, `python3`)
- `python sudoku_gui.py [SUDOKU_FILE]`
- To run with sample boards, click the `Generate Board` button. It will write over `sudoku_board.txt`