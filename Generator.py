import requests
from tabulate import tabulate

def generate():
    response = requests.get('https://sudoku-api.vercel.app/api/dosuku?query={newboard(limit:1){grids{value,solution,difficulty}}}')
    data = response.json()
    difficulty = data['newboard']['grids'][0]['difficulty']
    board_data = data['newboard']['grids'][0]['value']

    board = [['.' if cell == 0 else str(cell) for cell in row] for row in board_data]
    table = tabulate(board, tablefmt='plain')


    #write board into a .txt file
    with open('sudoku_board.txt', 'w') as f:
        for row in board:
            f.write(''.join(row) + '\n')

    return difficulty