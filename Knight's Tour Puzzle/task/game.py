import re
from typing import Optional, List


def show_board(rows: int, cols: int, board) -> None:
    h_length = len(str(rows))
    cell_size = len(str(rows * cols))
    print(" " * h_length + "-" * ((cell_size + 1) * cols + 3))
    for i in range(rows):
        print(f"{' ' * (h_length - len(str(rows - i)))}{rows - i}| {' '.join(board[i])} |")
    print(" " * h_length + "-" * ((cell_size + 1) * cols + 3))
    print(f'{" " * (h_length + 2)}'
          f'{" ".join([" " * (cell_size - 1) + str(i) for i in range(1, cols + 1)])}\n')


def input_position(rows: int, cols: int) -> tuple:
    while True:
        try:
            x, y = input().split()
            if re.search(r"^\d$", x) == False or re.search(r"^\d$", y) == False:
                raise ValueError

            x = int(x)
            y = int(y)

            if y > cols or y < 1 or x > rows or x < 1:
                raise ValueError
            return x - 1, -y

        except Exception:
            print("Invalid dimensions!")


def available_moves(board) -> List[tuple]:
    arr_indexes = []
    for i in range(len(board[0])):
        for j in range(len(board)):
            if board[j][i].strip().isdigit():
                arr_indexes.append((j - len(board), i))
    return arr_indexes


def is_win(rows: int, cols: int, board) -> bool:
    count_stars = 0
    count_x = 0
    for arr in board:
        count_stars += arr.count("*")
        count_x += arr.count(" X")

    if rows * cols - 1 == count_stars and count_x == 1:
        return True
    return  False


def input_size_board() -> tuple:
    while True:
        try:
            rows, cols = input("Enter your board dimensions: ").split()
            if re.search(r"^\d$", cols) == False or re.search(r"^\d$", rows) == False:
                raise ValueError

            rows = int(rows)
            cols = int(cols)

            if rows < 1 or cols < 1:
                raise ValueError
            return rows, cols

        except Exception:
            print("Invalid dimensions!")


def create_board(rows: int, cols: int):
    cell_size = len(str(rows * cols))
    board = [['_' * cell_size for _ in range(cols)] for _ in range(rows)]
    return board


def possible_moves(y: int, x: int, board, recursion=False, star_y=0, star_x=0) -> Optional[int]:
    cell_size = len(str(rows * cols))
    copy_board = create_board(cols, rows)
    if recursion:
        try:
            copy_board[y][x] = "X"
            for i in range(len(BOARD[0])):
                for j in range(len(BOARD)):
                    if BOARD[j][i].strip() == "*":
                        copy_board[j - len(BOARD)][i] = ' ' * (cell_size - 1) + "*"
            copy_board[star_y][star_x] = ' ' * (cell_size - 1) + "*"
        except IndexError:
            return 0

    counter_moves = 0
    k = u = 1
    q = -1
    g = 2
    for i in range(8):
        try:
            if not recursion:
                if (y - u * q) >= 0 or (x - g * k) < 0 or board[y - u * q][x - g * k].strip() == "*":
                    raise IndexError
                counter_moves = possible_moves((y - u * q), (x - g * k), copy_board, True, y, x)
                if counter_moves >= 0:
                    board[y - u * q][x - g * k] = ' ' * (cell_size - 1) + f"{counter_moves}"
            else:
                if (y - u * q) >= 0 or (x - g * k) < 0 or copy_board[y - u * q][x - g * k].strip() == "*":
                    raise IndexError
                copy_board[y - u * q][x - g * k] = ' ' * (cell_size - 1) + "O"
                counter_moves += 1
        except Exception:
            pass
        k *= -1
        q *= -1
        if i == 1:
            k = q = 1
        elif i == 3:
            k = 1
            q = -1
            g, u = u, g
        elif i == 5:
            k = q = 1

    return counter_moves


def knight_visited(board) -> int:
    unswer = 0
    for arr in board:
        count_x = arr.count("X")
        count_stars = arr.count("*")
        unswer = unswer + (count_x + count_stars)
    return unswer


def solve_the_puzzle(rows: int, cols: int, x: int, y: int, board):
    cell_size = len(str(rows * cols))
    board[y][x] = ' ' * (cell_size - 1) + "X"
    copy_board = [arr.copy() for arr in board]
    possible_moves(y, x, copy_board)
    board[y][x] = "*"
    text_move = "Enter your next move: "
    while True:

        if len(available_moves(copy_board)) == 0:
            if is_win(rows, cols, copy_board):
                show_board(cols, rows, copy_board)
                print("What a great tour! Congratulations!")
                exit(0)

            show_board(cols, rows, board)
            print("No more possible moves!")
            print(f"Your knight visited {knight_visited(board)} squares!")
            exit(-1)

        show_board(cols, rows, copy_board)
        print(text_move, end="")
        text_move = "Enter your next move: "
        x, y = input_position(rows, cols)
        if (y, x) not in available_moves(copy_board) or board[y][x] == "*":
            text_move = "Invalid move! Enter your next move: "
            continue

        board[y][x] = ' ' * (cell_size - 1) + "X"
        copy_board = [arr.copy() for arr in board]
        possible_moves(y, x, copy_board)
        board[y][x] = "*"


def isSafe(x, y, rows, cols, board):
	if(x >= 0 and y >= 0 and x < rows and y < cols and re.search(r"\D+", board[x][y].strip())):
		return True
	return False


def not_solve_the_puzzle(rows: int, cols: int):
    board = create_board(rows, cols)
    cell_size = len(str(rows * cols))

    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    board[0][0] = ' ' * (cell_size - 1) + f"{1}"

    pos = 2


    if (not solveKTUtil(rows, cols, board, 0, 0, move_x, move_y, pos)):
        return "No solution exists!"
    else:
        print("Here's the solution!")
        show_board(rows, cols, board)


def solveKTUtil(n, m, board, curr_x, curr_y, move_x, move_y, pos):
    cell_size = len(str(rows * cols))
    if (pos == n * m + 1):
        return True

    # Try all next moves from the current coordinate x, y
    for i in range(8):
        new_x = curr_x + move_x[i]
        new_y = curr_y + move_y[i]
        if (isSafe(new_x, new_y, rows, cols, board)):
            board[new_x][new_y] = ' ' * (cell_size - 1) + f"{pos}"
            if (solveKTUtil(n, m, board, new_x, new_y, move_x, move_y, pos + 1)):
                return True

            # Backtracking
            board[new_x][new_y] = '_' * cell_size
    return False


def is_correct_size(rows, cols) -> bool:
    if min(rows, cols) != 5:
        return False
    return True



if __name__ == "__main__":
    rows, cols = input_size_board()

    BOARD = create_board(cols, rows)
    print("Enter the knight's starting position: ", end="")
    x, y = input_position(rows, cols)
    while True:
        user_chice = input("Do you want to try the puzzle? (y/n): ")
        if user_chice == "y":
            unswer = not_solve_the_puzzle(rows, cols)
            if unswer is not None:
                print(unswer)
                break

            solve_the_puzzle(rows, cols, x, y, BOARD)
            break
        elif user_chice == "n":
            unswer = not_solve_the_puzzle(rows, cols)
            if unswer is not None:
                print(unswer)
            break
        else:
            print("Invalid input!")
