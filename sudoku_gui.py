import pygame
import time
import sys
import textwrap
from Generator import generate
from solver_method_1 import SudokuSolver1
from solver_method_2 import SudokuSolver2

pygame.init()

global screen_width, screen_height, screen, font, tab_0, tab_1, tab_2, tab_3, statistics_tab, board_1, board_2

# initialize display window size, tabs, boards
def gui_setup():
    global screen_width, screen_height, screen, font, tab_0, tab_1, tab_2, tab_3, statistics_tab, board_1, board_2

    screen_width = 800
    screen_height = 600

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sudoku")

    font = pygame.font.SysFont(None, 30)

    tab_0 = pygame.Rect(5, 5, 165, 40)  
    tab_1 = pygame.Rect(175, 5, 168, 40)
    tab_2 = pygame.Rect(348, 5, 210, 40)
    tab_3 = pygame.Rect(615, 5, 180, 40)
    # statistics_tab = pygame.Rect(563, 5, 115, 40)

    board_1 = None
    board_2 = None

def draw_intro():
    rules_rect = pygame.Rect(83, 207, 635, 185)
    pygame.draw.rect(screen, (211, 211, 211), rules_rect.move(4, 4))
    pygame.draw.rect(screen, (255, 255, 255), rules_rect)
    
    font = pygame.font.SysFont('Arial', 20)
    text = "Sudoku is a game consisting of a 9x9 grid, with 9 separate 3x3 subgrids. The rules of the game are simple. Each row, column, and 3x3 subgrid must be filled out with numbers 1-9 without numbers repeating in any row, column, or subgrid."
    lines = textwrap.wrap(text, width=65)

    y = 225
    for line in lines:
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (rules_rect.x + 20, y))
        y += 40

    pygame.display.update()

# draw tabs and format them
def draw_tabs():
    shadow_offset = 4
    shadow_color = (211, 211, 211)
    
    # draw shadows for the tabs
    pygame.draw.rect(screen, shadow_color, tab_0.move(shadow_offset, shadow_offset))
    pygame.draw.rect(screen, shadow_color, tab_1.move(shadow_offset, shadow_offset))
    pygame.draw.rect(screen, shadow_color, tab_2.move(shadow_offset, shadow_offset))
    pygame.draw.rect(screen, shadow_color, tab_3.move(shadow_offset, shadow_offset))
    # pygame.draw.rect(screen, shadow_color, statistics_tab.move(shadow_offset, shadow_offset))
    
    # draw the tabs
    pygame.draw.rect(screen, (255, 255, 255), tab_0)
    pygame.draw.rect(screen, (255, 255, 255), tab_1)
    pygame.draw.rect(screen, (255, 255, 255), tab_2)
    pygame.draw.rect(screen, (255, 255, 255), tab_3)
    # pygame.draw.rect(screen, (255, 255, 255), statistics_tab)

    # tab labels
    tab_0_text = font.render("Original Board", True, (0, 0, 0))
    tab_1_text = font.render("Human Method", True, (0, 0, 0))
    tab_2_text = font.render("Logic Programming", True, (0, 0, 0))
    tab_3_text = font.render("Generate Board", True, (0, 0, 0))
    # statistics_tab_text = font.render("Statistics", True, (0, 0, 0))

    screen.blit(tab_0_text, (tab_0.x + 10, tab_0.y + 10))
    screen.blit(tab_1_text, (tab_1.x + 10, tab_1.y + 10))
    screen.blit(tab_2_text, (tab_2.x + 10, tab_2.y + 10))
    screen.blit(tab_3_text, (tab_3.x + 10, tab_3.y + 10))
    # screen.blit(statistics_tab_text, (statistics_tab.x + 10, statistics_tab.y + 10))

# draw board given origin position (x,y) [top-left corner of the screen]
def draw_board(board, x=7, y=140):
    for i in range(9):
        for j in range(9):
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
                else:
                    text = font.render(str(board[i][j]), True, (255, 255, 255))
                screen.blit(text, (x + j * 50 + 15, y + i * 50 + 15))

    pygame.draw.rect(screen, (255, 255, 255), (x, y, 450, 450), 3)

    for i in range(10):
        if i % 3 == 0:
            thickness = 3
        else:
            thickness = 1
        pygame.draw.line(screen, (255, 255, 255), (x + i * 50, y), (x + i * 50, y + 450), thickness)
        pygame.draw.line(screen, (255, 255, 255), (x, y + i * 50), (x + 450, y + i * 50), thickness)

def board_highlight(board):
    indices = []
    for i in range(9):
        for j in range(9):
            if "0;31m" in str(board[i][j]):
                indices.append([i,j])
    return indices

def draw_highlight(board, indices):
    board = [[str(i) for i in line] for line in board]
    for i in range(9):
        for j in range(9):
            if [i,j] in indices: 
                board[i][j] = str(board[i][j]) + "0;31m"
    return board

# statistics for the statistics page
def display_statistics(runtime_1, runtime_2):
    statistics_text_1 = font.render(f'Human Method (Seconds): {runtime_1}', True, (255, 255, 255))
    statistics_text_2 = font.render(f'Logical Programming (Seconds): {runtime_2}', True, (255, 255, 255))
    screen.blit(statistics_text_1, (50, 150))
    screen.blit(statistics_text_2, (50, 200))

# statistics for the human method page
def display_human_stats(runtime_1, stack_calls):
    statistics_text_1 = font.render(f'Runtime (Seconds): {runtime_1}', True, (255, 255, 255))
    stack_calls_1 = font.render(f'Number of Stack Calls: {stack_calls}', True, (255, 255, 255))
    screen.blit(statistics_text_1, (5, 90))
    screen.blit(stack_calls_1, (5, 115))

# statistics for the logical programming method page
def display_logic_stats(runtime_2):
    statistics_text_2 = font.render(f'Runtime (Seconds): {runtime_2}', True, (255, 255, 255))
    stack_calls_2 = font.render(f'Number of Stack Calls: N/A', True, (255, 255, 255))
    screen.blit(statistics_text_2, (5, 90))
    screen.blit(stack_calls_2, (5, 115))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("ERROR: No specified file to solve. Add it in the command line arguments")
        exit()
    try:
        solver1 = SudokuSolver1(sys.argv[1])
        solver2 = SudokuSolver2(sys.argv[1])
    except Exception as e:
        print("ERROR: Invalid file")
        exit()

    # run solver 1
    runtime_1 = 0
    start_time = time.time()
    if solver1.solve(solver1.grid):
        end_time = time.time()
        runtime_1 = round(end_time - start_time, 3)
    else:
        print("ERROR: No solution")

    # run solver 2
    runtime_2 = 0
    start_time = time.time()
    solver2_board = solver2.solve_puzzle()
    end_time = time.time()
    runtime_2 = round(end_time - start_time, 3)

    indices = board_highlight(solver1.grid)
    solver2_board = draw_highlight(solver2_board, indices)

    # initialize gui
    gui_setup()
    # set event loop for gui
    initial = 0
    while True:
        for event in pygame.event.get():
            if initial == 0:
                draw_intro()
            draw_tabs()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                # if "original board" tab is pressed
                if tab_0.collidepoint(pos):
                    initial = 1
                    screen.fill((0,0,0))
                    draw_tabs()
                    draw_board(solver2.board)
                # if "human method" tab is pressed
                elif tab_1.collidepoint(pos):
                    initial = 1
                    screen.fill((0,0,0))
                    draw_tabs()
                    display_human_stats(runtime_1, solver1.num_stack_calls)
                    draw_board(solver1.grid)
                # logic programming is pressed
                elif tab_2.collidepoint(pos):
                    initial = 1
                    screen.fill((0,0,0))
                    draw_tabs()
                    display_logic_stats(runtime_2)
                    draw_board(solver2_board)
                # generate board
                elif tab_3.collidepoint(pos):
                    initial = 1
                    screen.fill((0,0,0))
                    draw_tabs()
                    
                    generate()

                    solver1 = SudokuSolver1("sudoku_board.txt")
                    solver2 = SudokuSolver2("sudoku_board.txt")

                    runtime_1 = 0
                    start_time = time.time()
                    if solver1.solve(solver1.grid):
                        end_time = time.time()
                        runtime_1 = round(end_time - start_time, 3)
                    else:
                        print("ERROR: No solution")

                    # run solver 2
                    runtime_2 = 0
                    start_time = time.time()
                    solver2_board = solver2.solve_puzzle()
                    end_time = time.time()
                    runtime_2 = round(end_time - start_time, 3)

                    indices = board_highlight(solver1.grid)
                    solver2_board = draw_highlight(solver2_board, indices)

                    draw_board(solver2.board)
                # stastics tab is pressed
                # elif statistics_tab.collidepoint(pos):
                #     initial = 1
                #     screen.fill((0,0,0))
                #     draw_tabs()
                #     display_statistics(str(runtime_1), str(runtime_2))
        pygame.display.update()