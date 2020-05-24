import tictactoe as ttt


def print_board(b):
    for row in b:
        print(row)


board = ttt.initial_state()
print_board(board)


while not ttt.terminal(board):
    if ttt.player(board) == "X":
        x = int(input("Enter the row: "))
        y = int(input("Enter the column: "))

        if board[x-1][y-1] is None:
            board[x-1][y-1] = "X"
            print_board(board)
        continue

    if ttt.player(board) == "O":
        print("waiting for AI...")
        cell = ttt.minimax(board)
        board[cell[0]][cell[1]] = "O"
        print_board(board)








