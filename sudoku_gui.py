import pygame
import time
import sys
import textwrap
import numpy as np
from Generator import generate
from solver_method_1 import SudokuSolver1
from solver_method_2 import SudokuSolver2

pygame.init()

global screen_width, screen_height, screen, font, tab_0, tab_1, tab_2, tab_3, statistics_tab, board_1, board_2, difficulty

# initialize display window size, tabs, boards
def gui_setup():
    global screen_width, screen_height, screen, font, tab_0, tab_1, tab_2, tab_3, statistics_tab, board_1, board_2, difficulty

    # display window dimensions
    screen_width = 800
    screen_height = 600

    # set display dimensions
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sudoku")

    # specify font size
    font = pygame.font.SysFont(None, 30)

    # specify tab sizes
    tab_0 = pygame.Rect(5, 5, 165, 40)  
    tab_1 = pygame.Rect(175, 5, 168, 40)
    tab_2 = pygame.Rect(348, 5, 210, 40)
    statistics_tab = pygame.Rect(563, 5, 115, 40)
    tab_3 = pygame.Rect(610, 545, 180, 40)

    # set boards to empty initially
    board_1 = None
    board_2 = None

    # set difficulty to none initially
    difficulty = None

# generates intro screen of the gui, explaining the rules of sudoku
def draw_intro():
    # create text box for rules of sudoku
    rules_rect = pygame.Rect(83, 207, 635, 185)
    pygame.draw.rect(screen, (211, 211, 211), rules_rect.move(4, 4))
    pygame.draw.rect(screen, (255, 255, 255), rules_rect)
    # specify text font, and text-box contents
    font = pygame.font.SysFont('Arial', 20)
    text = "Sudoku is a game consisting of a 9x9 grid, with 9 separate 3x3 subgrids. The rules of the game are simple. Each row, column, and 3x3 subgrid must be filled out with numbers 1-9 without numbers repeating in any row, column, or subgrid."
    lines = textwrap.wrap(text, width=65)
    # ensure lines wrap instead of having one long string
    y = 225
    for line in lines:
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (rules_rect.x + 20, y))
        y += 40

    pygame.display.update()

# draw tabs and format them onto the screen neatly
def draw_tabs(selected_tab):
    # create a tab offset and color to make the tabs appear 3 dimensional
    shadow_offset = 4
    shadow_color = (211, 211, 211)
    
    # draw shadows for the tabs, using the screen, shadow color, and offset
    pygame.draw.rect(screen, shadow_color, tab_0.move(shadow_offset, shadow_offset))
    pygame.draw.rect(screen, shadow_color, tab_1.move(shadow_offset, shadow_offset))
    pygame.draw.rect(screen, shadow_color, tab_2.move(shadow_offset, shadow_offset))
    pygame.draw.rect(screen, shadow_color, tab_3.move(shadow_offset, shadow_offset))
    pygame.draw.rect(screen, shadow_color, statistics_tab.move(shadow_offset, shadow_offset))

    color = (255, 255, 255)
    
    # draw the tabs
    pygame.draw.rect(screen, color, tab_0)
    pygame.draw.rect(screen, color, tab_1)
    pygame.draw.rect(screen, color, tab_2)
    pygame.draw.rect(screen, color, tab_3)
    pygame.draw.rect(screen, color, statistics_tab)

    select_color = (200,200,200)

    # if the tab is selected, make the tab darker in color to emulate a pressed down tab
    if selected_tab == 0:
        pygame.draw.rect(screen, select_color, tab_0)
    elif selected_tab == 1:
        pygame.draw.rect(screen, select_color, tab_1)
    elif selected_tab == 2:
        pygame.draw.rect(screen, select_color, tab_2)
    elif selected_tab == 3:
        pygame.draw.rect(screen, select_color, tab_3)
    elif selected_tab == 4:
        pygame.draw.rect(screen, select_color, statistics_tab)

    # specify the text of the tabs/buttons
    tab_0_text = font.render("Original Board", True, (0, 0, 0))
    tab_1_text = font.render("Human Method", True, (0, 0, 0))
    tab_2_text = font.render("Logic Programming", True, (0, 0, 0))
    tab_3_text = font.render("Generate Board", True, (0, 0, 0))
    statistics_tab_text = font.render("Statistics", True, (0, 0, 0))

    # place the buttons onto the screen
    screen.blit(tab_0_text, (tab_0.x + 10, tab_0.y + 10))
    screen.blit(tab_1_text, (tab_1.x + 10, tab_1.y + 10))
    screen.blit(tab_2_text, (tab_2.x + 10, tab_2.y + 10))
    screen.blit(tab_3_text, (tab_3.x + 10, tab_3.y + 10))
    screen.blit(statistics_tab_text, (statistics_tab.x + 10, statistics_tab.y + 10))

# draw board given origin position (x,y) [top-left corner of the screen]
def draw_board(board, x=7, y=140):
    # iterate through the entire board, if the number was generated from the api, color it red to indicate the based board numbers
    for i in range(9):
        for j in range(9):
            # if the value is not zero, check if the number is supposed to be colored red, if so color red
            if board[i][j] != 0:
                # remove color highlighting from numbers
                if("0;31m" in str(board[i][j])):
                    board[i][j] = str(board[i][j]).replace("0;31m","")
                    board[i][j] = str(board[i][j]).replace("[","")
                    board[i][j] = str(board[i][j]).replace("0m","")
                    for k in str(board[i][j]):
                        if k not in "123456789":
                            board[i][j] = board[i][j].replace(k, "")
                    # color solution numbers in red
                    text = font.render(str(board[i][j]), True, (255, 114, 118))
                    board[i][j] = str(board[i][j]) + "0;31m"
                elif str(board[i][j]) == '.':
                    text = font.render('•', True, (255,255,255))
                else:
                    text = font.render(str(board[i][j]), True, (255, 255, 255))
                screen.blit(text, (x + j * 50 + 15, y + i * 50 + 15))

    pygame.draw.rect(screen, (255, 255, 255), (x, y, 450, 450), 3)

    # draw the lines of the sudoku board given vertex coordinates
    for i in range(10):
        if i % 3 == 0:
            thickness = 3
        else:
            thickness = 1
        pygame.draw.line(screen, (255, 255, 255), (x + i * 50, y), (x + i * 50, y + 450), thickness)
        pygame.draw.line(screen, (255, 255, 255), (x, y + i * 50), (x + 450, y + i * 50), thickness)

# indicate which numbers need to be highlted as the based board numbers for method2
def board_highlight(board):
    indices = []
    for i in range(9):
        for j in range(9):
            if "0;31m" in str(board[i][j]):
                indices.append([i,j])
    return indices

# highlight the based board numbers for method2
def draw_highlight(board, indices):
    board = [[str(i) for i in line] for line in board]
    for i in range(9):
        for j in range(9):
            if [i,j] in indices: 
                board[i][j] = str(board[i][j]) + "0;31m"
    return board

# calculates average runtime for both solvers
def performance(solver1, solver2, iterations = 10):
    solver1_runtime = []
    solver2_runtime = []
    # calculate the runtime for both solvers, 'iterations' ammount of times
    for i in range(iterations):
        runtime_1 = 0
        start_time = time.time()
        # solve for method 1, track runtime
        if solver1.solve(solver1.grid):
            end_time = time.time()
            runtime_1 = end_time - start_time
        else:
            print("ERROR: No solution")

        # run solver 2, calculate runtime
        runtime_2 = 0
        start_time = time.time()
        solver2_board = solver2.solve_puzzle()
        end_time = time.time()
        runtime_2 = end_time - start_time
        # add runtime to the list
        solver1_runtime.append(runtime_1)
        solver2_runtime.append(runtime_2)
    # return the average runtime for both solvers
    return [round(np.average(solver1_runtime),7), round(np.average(solver2_runtime),7)]

# statistics for the statistics page
def display_statistics(runtime_1, runtime_2, iterations, difficulty):
    # print statistics such as runtime on statistics tab
    statistics_difficulty = font.render(f'Board Difficulty: {difficulty}', True, (255,255,255))
    statistics_iterations = font.render(f'Iterations: {iterations}', True, (255,255,255))
    statistics_text_1 = font.render(f'Human Method Average Runtime (Seconds): {runtime_1}', True, (255, 255, 255))
    statistics_text_2 = font.render(f'Logical Programming Average Runtime (Seconds): {runtime_2}', True, (255, 255, 255))
    # specify stat location
    screen.blit(statistics_difficulty, (50, 100))
    screen.blit(statistics_iterations, (50, 150))
    screen.blit(statistics_text_1, (50, 200))
    screen.blit(statistics_text_2, (50, 250))

# statistics for the human method page
def display_human_stats(runtime_1, stack_calls):
    # display stats for the human method on the human tab
    statistics_text_1 = font.render(f'Runtime (Seconds): {runtime_1}', True, (255, 255, 255))
    stack_calls_1 = font.render(f'Number of Stack Calls: {stack_calls}', True, (255, 255, 255))
    screen.blit(statistics_text_1, (5, 90))
    screen.blit(stack_calls_1, (5, 115))

# statistics for the logical programming method page
def display_logic_stats(runtime_2):
    # display stats for the logic programming method on the logic programming tab
    statistics_text_2 = font.render(f'Runtime (Seconds): {runtime_2}', True, (255, 255, 255))
    stack_calls_2 = font.render(f'Number of Stack Calls: N/A', True, (255, 255, 255))
    screen.blit(statistics_text_2, (5, 90))
    screen.blit(stack_calls_2, (5, 115))

if __name__ == '__main__':
    # ensure coorect number of command lines arguments, and valid file
    if len(sys.argv) < 2:
        print("ERROR: No specified file to solve. Add it in the command line arguments")
        exit()
    try:
        solver1 = SudokuSolver1(sys.argv[1])
        solver2 = SudokuSolver2(sys.argv[1])
    except Exception as e:
        print("ERROR: Invalid file")
        exit()

    # run solver 1, track runtime
    runtime_1 = 0
    start_time = time.time()
    if solver1.solve(solver1.grid):
        end_time = time.time()
        runtime_1 = round(end_time - start_time, 3)
    else:
        print("ERROR: No solution")

    # run solver 2, track runtime
    runtime_2 = 0
    start_time = time.time()
    solver2_board = solver2.solve_puzzle()
    end_time = time.time()
    runtime_2 = round(end_time - start_time, 3)

    # highlight base board colors in red
    indices = board_highlight(solver1.grid)
    solver2_board = draw_highlight(solver2_board, indices)
    # specify iterations for average runtime
    iterations = 10
    performance_list = performance(solver1, solver2, iterations)

    # initialize gui
    gui_setup()
    # set event loop for gui
    initial = 0
    while True:
        for event in pygame.event.get():
            # draw intro screen only initially
            if initial == 0:
                draw_intro()
            draw_tabs(None)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                # if "original board" tab is pressed, draw original board
                if tab_0.collidepoint(pos):
                    initial = 1
                    screen.fill((0,0,0))
                    draw_tabs(0)
                    draw_board(solver2.board)
                # if "human method" tab is pressed, draw human method solution, runtime, and stack calls
                elif tab_1.collidepoint(pos):
                    initial = 1
                    screen.fill((0,0,0))
                    draw_tabs(1)
                    display_human_stats(runtime_1, solver1.num_stack_calls)
                    draw_board(solver1.grid)
                # logic programming is pressed, draw logic programming solution and runtime
                elif tab_2.collidepoint(pos):
                    initial = 1
                    screen.fill((0,0,0))
                    draw_tabs(2)
                    display_logic_stats(runtime_2)
                    draw_board(solver2_board)
                # generate board, create solvers for the new board, calculate runtime, draw new generated base board
                elif tab_3.collidepoint(pos):
                    initial = 1
                    screen.fill((0,0,0))
                    draw_tabs(3)
                    
                    # grab board difficulty from api
                    difficulty = generate()

                    # create solvers for new board given txt file
                    solver1 = SudokuSolver1("sudoku_board.txt")
                    solver2 = SudokuSolver2("sudoku_board.txt")

                    # use method 1 to solve board and calculate runtime
                    runtime_1 = 0
                    start_time = time.time()
                    if solver1.solve(solver1.grid):
                        end_time = time.time()
                        runtime_1 = round(end_time - start_time, 3)
                    else:
                        print("ERROR: No solution")

                    # use method 2 to solve board and calculate runtime
                    runtime_2 = 0
                    start_time = time.time()
                    solver2_board = solver2.solve_puzzle()
                    end_time = time.time()
                    runtime_2 = round(end_time - start_time, 3)

                    # highlight base board indices
                    indices = board_highlight(solver1.grid)
                    solver2_board = draw_highlight(solver2_board, indices)

                    # run performance function to get average runtime
                    performance_list = performance(solver1, solver2, iterations)

                    # generate board
                    draw_board(solver2.board)
                # stastics tab is pressed, display all statisticks (board diffculty, runtime, iterations)
                elif statistics_tab.collidepoint(pos):
                    initial = 1
                    screen.fill((0,0,0))
                    draw_tabs(4)
                    display_statistics(str(performance_list[0]), str(performance_list[1]), iterations, difficulty)
        pygame.display.update()