import time

# CHECK THIS OUT, THIS WORKS FOR HUGE BOARDS!!!
ROW_COUNT = 8
COLUMN_COUNT = 8


# This uses the numpy import to create a board that is ROW_COUNT wide and COLUMN_COUNT tall
# It sets all values as an int valued at 0
def create_board():
    board = []
    subBoard = []
    for x in range(ROW_COUNT + 1):
        if len(subBoard) >> 0:
            board.append(subBoard)
            subBoard = []
        for y in range(COLUMN_COUNT):
            subBoard.append(0)
    return board


# This determines whether the current move is the last move
def complete_check(step):
    global ROW_COUNT
    global COLUMN_COUNT
    if step == ROW_COUNT * COLUMN_COUNT:
        return True


# This tests whether the potential move is valid.
# It checks whether the move is on the board and the space has not been landed on previously (ie is zero).
def valid_move(x, y, board):
    if 0 <= x < ROW_COUNT and 0 <= y < COLUMN_COUNT and board[x][y] == 0:
        return True
    return False


# This is the main driver of the program. From top to bottom, this will:
# Update the second board generated to determine how many moves can be made from each cell.
# Next, it will find the move available from the current space that has the fewest possible moves onward.
# Then, for all listed knight moves it checks whether the move is on the board, has not been previously landed,
    # the iterator is greater than any iterations from this space that required a backtrack, and
    # the move is to the most constrained of possible next spaces.
# If all the previous steps conditions are met, this takes the move by increasing x and y by the move values.
# Then, it updates the space to indicate that it has been moved to and updates the list of moves taken.
# Next, it resets the variable used to store the iterator from which the function backtracked.
# Then, this function tests whether the board is final by comparing the current move number to the size of the board.
# Next, this will determine whether there is a next move available, and if so, take that move by recurring.
# If there are no next moves available, this converts the current space back to zero.
# It then moves back to the previous space based on the (x, y) values from the last entry to the list of moves.
# Then, this sets the variable to track backtrack iterations to the current iterator plus one.
# Then, this function removes the latest move from the list of moves and
    # adds one to the variable to track number of failed paths.
# If there is no successful path found, this function returns False.
def tour_function(x, y, board, pos, tracker_list):
    global a
    global z

    populate_efficiency(effeciency_board, ROW_COUNT, COLUMN_COUNT, board)
    n = most_constrained(effeciency_board, x, y, board)

    for m in range(len(moves)):
        if valid_move(x + moves[m][0], y + moves[m][1], board) and m >= a and moves[m] == n:
            x += moves[m][0]
            y += moves[m][1]
            board[x][y] = pos
            tracker_list.append(m)
            a = 0
            if complete_check(pos):
                print(str(z) + " attempts made to find path.")
                return True
            if tour_function(x, y, board, pos + 1, tracker_list):
                return True
            board[x][y] = 0
            x -= moves[tracker_list[-1]][0]
            y -= moves[tracker_list[-1]][1]
            a = tracker_list[-1] + 1
            tracker_list.pop()
            z += 1
    return False


# This generates a number for each space. That number shows how many valid moves there are from that space.
def populate_efficiency(board, row, col, tour_board):
    for x in range(row):
        for y in range(col):
            eff_counter = 0
            for m in moves:
                if valid_move(x + int(m[0]), y + int(m[1]), tour_board):
                    eff_counter += 1
            board[x][y] = eff_counter
    return effeciency_board


# This function creates a list which is only used in this function.
# For all listed knight moves, this function checks whether the listed move results in a move on the board that also has
    # not been visited yet.
# For any moves that meet the above conditions, it adds the number of moves available from that valid space.
# Then for all listed knight moves, this checks whether the move is to a space on the board that has not been visited
    # and has the same number of moves as the valid move space with the fewest next moves available.
# This function then returns the (x, y) values for that knight move.
def most_constrained(eff_board, x_pos, y_pos, tour_board):
    cons_options = []
    for m in moves:
        if valid_move(x_pos + m[0], y_pos + m[1], tour_board):
            cons_options.append(eff_board[x_pos + m[0]][y_pos + m[1]])
    cons_options.sort()
    for cm in moves:
        if valid_move(x_pos + cm[0], y_pos + cm[1], tour_board) and \
                eff_board[x_pos + cm[0]][y_pos + cm[1]] == cons_options[0]:
            return cm

# This gets the time and prints it in the format: Hours, minutes, seconds
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print(current_time)
# This creates a the board that will show the knight's path
board = create_board()
# This is the list of knight's possible moves
moves = [[1, 2], [2, 1], [1, -2], [2, -1], [-1, 2], [-1, -2], [-2, 1], [-2, -1]]
# This creates the board that tracks how many moves are available from each space.
effeciency_board = create_board()
a = 0
z = 0
x = 0
y = 0
# This is to set up the first move. pos is used to show the order of moves taken in the path.
pos = 1
tracker_list = [0]
board[x][y] = pos
pos += 1
# This calls the tour_function. If a solution is possible, it prints the path and ending time of the program.
if tour_function(x, y, board, pos, tracker_list):
    print("Tour Complete")
    for row in board:
        print(*row)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)
else:
    print("No Tour Exists")
