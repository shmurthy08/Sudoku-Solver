import requests
from tabulate import tabulate

generated_file_name = 'sudoku_board.txt'

def generate():
    # Send a GET request to the Sudoku API to retrieve puzzle data
    response = requests.get('https://sudoku-api.vercel.app/api/dosuku?query={newboard(limit:1){grids{value,solution,difficulty}}}')
    data = response.json()

    # Extract the difficulty level and the puzzle grid from the API response
    difficulty = data['newboard']['grids'][0]['difficulty']
    board_data = data['newboard']['grids'][0]['value']

    # Convert the puzzle grid into a 2D list representation
    # Replace 0s with '.' for empty cells or keep the number as a string
    board = [['.' if cell == 0 else str(cell) for cell in row] for row in board_data]

    # Generate a table representation of the board using tabulate library
    table = tabulate(board, tablefmt='plain')

    # Write the board into a text file named 'sudoku_board.txt'
    with open(generated_file_name, 'w') as f:
        for row in board:
            f.write(''.join(row) + '\n')

    # Return the difficulty level
    return difficulty

if __name__ == '__main__':
    print(f"New board generated at '{generated_file_name}' with {generate()} difficulty")