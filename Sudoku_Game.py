import numpy
from numpy import random
import pygame
import sys
import math
import copy

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (200, 200, 200)
BUTTON = (100, 100, 100)

# Making a possibility for bigger Sudoku?
Root_of_Rows = 2
ROW_COUNT = Root_of_Rows * Root_of_Rows
COLUMN_COUNT = ROW_COUNT
List_Possible = []
user_good_input = False
user_value = 0
all_cells_entered = False
squares = []
poss_mod = 0
toggle = 0
square_number = 0
squares_index = [[]]
cell = 0
solvable_ind = False
ROW_TRUE = False
COLUMN_TRUE = False
SQUARE_MASTER = [[]]
SQUARE_TRUE = False

# This creates a list of unique values needed in each row / column / square for valid solution
# The append(r + 1) bit is so that the list starts at 1 and increments to the ROW_COUNT value
# TEST_LIST looks at each row / column / square. TEST_MASTER is a list of all TEST_LISTS, so entire puzzle
TEST_LIST = []
TEST_MASTER = [[]]
for r in range(ROW_COUNT):
    TEST_LIST.append(r + 1)
for c in range(ROW_COUNT * COLUMN_COUNT):
    if c > 0 and (c + 1) % (len(TEST_LIST)) == 0:
        TEST_MASTER.append(TEST_LIST)

# Creates a board that is determined by the row and column lengths determined above
def create_board():
    board = numpy.zeros((ROW_COUNT, COLUMN_COUNT), dtype = int)
    return board

# Function that returns true if there are only non-zero values in all cells of board.
# Use this loop after the number entry to determine whether the puzzle is solved
# If the display board does not equal the list_possibles (which became the answer key) then this deletes errors
def all_cells_check(board):
    global all_cells_entered
    i = 0
    e = 0
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] != 0 and board[r][c] == List_Possible[(r * len(TEST_LIST)) + c]:
                i += 1
            elif board[r][c] != 0:
                e += 1
                i += 1
            else:
                pass
        if e > 0 and i == (ROW_COUNT * COLUMN_COUNT):
            for c in range(COLUMN_COUNT):
                for r in range(ROW_COUNT):
                    if board[r][c] != List_Possible[(r * len(TEST_LIST)) + c]:
                        board[r][c] = 0
                        draw_board(board)
                        pygame.display.update()
                    else:
                        pass
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            pygame.draw.rect(screen, BLACK, (0, 0, SQUARESIZE, height))
            pygame.display.update()
            font = pygame.font.SysFont('courier', 15)
            label = font.render('Errors erased, keep trying!', 1, YELLOW)
            cellx = (SQUARESIZE / 2)
            celly = (SQUARESIZE / 2)
            screen.blit(label, (int(cellx), int(celly)))
            pygame.display.update()
            pygame.time.wait(2000)
        elif e == 0 and i == (ROW_COUNT * COLUMN_COUNT):
            all_cells_entered = True
        else:
            pass

# This was a doozy for me, lots of stuff in here.
# Basically, it organizes all the rows, columns, and squares values to test against the TEST_MASTER list values.
# A little more detail, it organizes each value in each row as a sorted sublist in ROW_MASTER
# This does the same sorted sublisting for columns and squares
# Then it compares those three lists to the TEST_MASTER
# If all four are the same, then this makes the solvable indicator set to True.
# This is used with the start values function to brute force a valid grid.
def solvable_test(List):
    global solvable_ind
    global ROW_TRUE
    global COLUMN_TRUE
    global SQUARE_TRUE
    i = 0
    ROW_MASTER = [[]]
    ROW_FIRST = []
    COLUMN_MASTER = [[]]
    COLUMN_FIRST = []
    ROW_TRUE = False
    COLUMN_TRUE = False
    for l in List:
        if type(l) == int:
            i += 1
    if i == (ROW_COUNT * COLUMN_COUNT):
        for r in range(len(List_Possible)):
            ROW_FIRST.append(List_Possible[r])
            if r > 0 and (r + 1) % len(TEST_LIST) == 0:
                ROW_FIRST.sort()
                ROW_MASTER.append(ROW_FIRST)
                ROW_FIRST = []
        t = 0
        for value in range(len(List_Possible)):
            h = value % len(TEST_LIST)
            if h == 0 and value == 0:
                w = 0
            elif h == 0 and value > 0:
                w = t
            elif h != 0 and h != (len(TEST_LIST) - 1):
                w = (h * len(TEST_LIST)) + t
            else:
                w = (h * len(TEST_LIST)) + t
                t += 1
            COLUMN_FIRST.append(List_Possible[w])
            if value > 0 and (value + 1) % len(TEST_LIST) == 0:
                COLUMN_FIRST.sort()
                COLUMN_MASTER.append(COLUMN_FIRST)
                COLUMN_FIRST = []
        assign_squares()
        if SQUARE_MASTER == TEST_MASTER:
            SQUARE_TRUE = True
        if ROW_MASTER == TEST_MASTER:
                ROW_TRUE = True
        if COLUMN_MASTER == TEST_MASTER:
                COLUMN_TRUE = True
        if ROW_TRUE == True and COLUMN_TRUE == True and SQUARE_TRUE == True:
            solvable_ind = True
        else:
            restart(board, List_Possible)
    else:
        pass

# Function that creates a list of possible values for every cell
# Uses a deep copy of the TEST_LIST so that list in list edits can occur later
def generate_possibles():
    global TEST_LIST
    global List_Possible
    List_Possible = []
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            List_Possible.append(copy.deepcopy(TEST_LIST))

# This takes the location of mouse click in the main while loop and puts it in the numpy board format
# It takes a user-entered value and updates the display
# user_good_input is reset so that the while loop in another def is primed for when user clicks screen
def value_entered(board):
    global gridx
    global gridy
    global user_good_input
    global user_value
    board[((int((gridy / SQUARESIZE) - 1)))][(int((gridx / SQUARESIZE) - 1))] = user_value
    user_good_input = False
    draw_board(board)

# Makes a list of lists of the values in different boxes (which I call squares also) for the dynamic puzzle size
# The numbers in the lists are the values from cells as if numbered off reading from right to left, up to down.
# For example, in a 2 x 2 grid, cells 1, 2, 4, and 5 would be in the first square. Next square would be 3, 4, 6, and 7.
# This list would, thus, show the values for cells 1, 2, 4, and 5 from the List_Possibles as the first sublist.
# This cycles through the number of squares according to the TEST_LIST in the row direction, then through columns.
def assign_squares():
    global squares
    global SQUARE_MASTER
    i = 0
    square_run = 0
    new_square = 0
    row_run = 0
    squares = []
    for x in range(len(TEST_LIST)):
        for r in range(Root_of_Rows):
            row = r + (row_run * Root_of_Rows)
            for c in range(Root_of_Rows):
                col = c + (new_square * Root_of_Rows)
                squares.append(int(List_Possible[(row * len(TEST_LIST)) + col]))
                i += 1
                if i % Root_of_Rows == 0:
                    square_run += 1
                    if square_run == Root_of_Rows:
                        new_square += 1
                        square_run = 0
                        squares.sort()
                        SQUARE_MASTER.append(squares)
                        squares = []
                        if new_square % Root_of_Rows == 0:
                            new_square = 0
                            row_run += 1
                        else:
                            pass
    else:
        pass

# Makes a list of lists of the cell numbers in different boxes (which I call squares also) for the dynamic puzzle size
# The cells are numbered as if reading from right to left, up to down.
# For example, in a 2 x 2 grid, cells 1, 2, 4, and 5 would be in the first square. Next square would be 3, 4, 6, and 7.
# This list would, thus, show cells 1, 2, 4, and 5 as the first sublist.
# This cycles through the number of squares according to the TEST_LIST in the row direction, then through columns.
# At the end, this deletes a blank sublist from index [0] due to append work instead of inserts.
def squares_for_possibles():
    global squares_index
    i = 0
    square_run = 0
    new_square = 0
    row_run = 0
    squares = []
    for x in range(len(TEST_LIST)):
        for r in range(Root_of_Rows):
            row = r + (row_run * Root_of_Rows)
            for c in range(Root_of_Rows):
                col = c + (new_square * Root_of_Rows)
                squares.append(int((row*len(TEST_LIST))+(col)))
                i += 1
                if i % Root_of_Rows == 0:
                    square_run += 1
                    if square_run == Root_of_Rows:
                        new_square += 1
                        square_run = 0
                        squares_index.append(squares)
                        squares = []
                        if new_square % Root_of_Rows == 0:
                            new_square = 0
                            row_run += 1
                        else:
                            pass
    if len(squares_index[0]) == 0:
        del squares_index[0]
    else:
        pass

# There are two buttons that are drawn below the puzzle, which will have separate functions called if clicked
# This will draw a board based on the the puzzle dimensions.
# This will draw a black line for all borders that run along a square (which requires unique numbers inside)
# The other lines are drawn with blue
# This also generates a red circle that follows the mouse on a static y-value, a yellow dot does the same for x-value
def draw_board(board):
    pygame.draw.rect(screen,
                     BUTTON,
                     (int(SQUARESIZE), int(height - (SQUARESIZE / 2)),
                       int(SQUARESIZE), int(height)),
                     1)
    pygame.draw.rect(screen,
                     BUTTON,
                     (int(SQUARESIZE), int(height - SQUARESIZE),
                       int(SQUARESIZE), int(height - (SQUARESIZE / 2))), 1)

    font = pygame.font.SysFont('courier', 15)
    Check_label = font.render('C', 1, GREEN)
    screen.blit(Check_label, (int(1.5 * SQUARESIZE), int(height - ((4 * SQUARESIZE) / 4))))
    Toggle_label = font.render('P', 1, GREEN)
    screen.blit(Toggle_label, (int(1.5 * SQUARESIZE), int(height - ((2 * SQUARESIZE) / 4))))

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen,
                             WHITE,
                             (SQUARESIZE, SQUARESIZE,
                              c*SQUARESIZE + SQUARESIZE, r*SQUARESIZE + SQUARESIZE)
                             )
            for y in range(COLUMN_COUNT):
                if y % Root_of_Rows == 0:
                    pygame.draw.line(
                        screen,
                        BLACK,
                        ((y + 1) * SQUARESIZE, SQUARESIZE),
                        (((y + 1) * SQUARESIZE), ((ROW_COUNT + 1) * SQUARESIZE))
                    )
                else:
                    pygame.draw.line(
                        screen,
                        BLUE,
                        ((y + 1) * SQUARESIZE, SQUARESIZE),
                        (((y + 1) * SQUARESIZE), ((ROW_COUNT + 1) * SQUARESIZE))
                    )
                for x in range(ROW_COUNT):
                    if x % Root_of_Rows == 0:
                        pygame.draw.line(screen,
                                     BLACK,
                                     (SQUARESIZE, ((x + 1) * SQUARESIZE)),
                                     (((COLUMN_COUNT + 1) * SQUARESIZE), ((x + 1) * SQUARESIZE))
                                     )
                    else:
                        pygame.draw.line(screen,
                                         BLUE,
                                         (SQUARESIZE, ((x + 1) * SQUARESIZE)),
                                         (((COLUMN_COUNT + 1) * SQUARESIZE), ((x + 1) * SQUARESIZE))
                                         )

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            font = pygame.font.SysFont('comicsans', 30)
            if board[r][c] != 0:
                label = font.render(str(int(board[r][c])), 1, BLACK)
                cellx = ((c * SQUARESIZE) + (int(3 * SQUARESIZE)) / 2)
                celly = ((r * SQUARESIZE) + (int(3 * SQUARESIZE)) / 2)
                screen.blit(label, (int(cellx), int(celly)))

# This identifies the square number for a given x, y pair (by index) in the list developed by assign_squares function
def get_square_number(x, y):
    global square_number
    global squares_index
    cell_number = ((x * len(TEST_LIST)) + y)
    i = 0
    for z in squares_index:
        if cell_number in z:
            square_number = i
            i += 1
        else:
            i += 1

# This generates starting values for the puzzle and prints to the board
# This approach is very brute force and relies on randomly generated values
# This will randomly assign an x and a y value and determine whether that cell has multiple possible entries
# If there are not multiple, it chooses another x, y pair.
# If there are multiple then a random value of those values is assigned.
# Then all possible values in the row, cell, and square are removed based on the assigned value.
# Next, cells that have only one possible value are converted to an int in the List_Possibles
# For int values in the List_Possibles, this removes that int value from the rows / columns / squares possibles
# Then if a cells list of possibles is reduced to no options, the board is restarted.
# After all that, this checks to see whether the puzzle is solvable using a separate function.
# If that function returns the puzzle is solvable, this while loop breaks and the puzzle is generated.
def start_values(board, List_Possible):
    global squares_index
    global square_number
    global cell
    global solvable_ind
    global ROW_TRUE
    global COLUMN_TRUE
    n = 0
    while solvable_ind == False:
        x = ((random.choice(TEST_LIST)) - 1)
        y = ((random.choice(TEST_LIST)) - 1)
        a = x * len(TEST_LIST)
        b = (((x + 1) * len(TEST_LIST)) - 1)
        c = (len(TEST_LIST) - y)
        if type(List_Possible[(a + y)]) == list and len(List_Possible[(a + y)]) > 1 and board[x][y] == 0:
            board[x][y] = random.choice(List_Possible[(a + y)])
            List_Possible[(a + y)] = int(board[x][y])
            cell = int(board[x][y])
            draw_board(board)
            pygame.display.update()
            get_square_number(x, y)
            for iteration, z in enumerate(List_Possible):
                if a <= iteration <= b and type(z) == list:
                    if cell in z:
                        z.remove(cell)
                if (iteration + c) % (len(TEST_LIST)) == 0 and type(z) == list:
                    if cell in z:
                        z.remove(cell)
                if iteration in squares_index[square_number] and type(z) == list:
                    if cell in z:
                        z.remove(cell)
                for iterate, l in enumerate(List_Possible):
                    if type(l) != int and len(l) == 1:
                        z = List_Possible[iterate].pop()
                        List_Possible[iterate] = z
                        x = iterate // len(TEST_LIST)
                        y = iterate % len(TEST_LIST)
                        a = (x * len(TEST_LIST))
                        b = (((x + 1) * len(TEST_LIST)) - 1)
                        c = (len(TEST_LIST) - y)
                        get_square_number(x, y)
                        for ite, q in enumerate(List_Possible):
                            if a <= ite <= b and type(q) != int:
                                if z in q:
                                    q.remove(z)
                            if (ite + c) % (len(TEST_LIST)) == 0 and type(q) != int:
                                if z in q:
                                    q.remove(z)
                            if ite in squares_index[square_number] and type(q) != int:
                                if z in q:
                                    q.remove(z)
                    else:
                        pass
            for l in List_Possible:
                if type(l) == int:
                    pass
                elif len(l) == 0:
                    restart(board, List_Possible)
                else:
                    pass
            solvable_test(List_Possible)
        else:
            solvable_test(List_Possible)

# If other functions get to an invalid puzzle state, this restarts the board and list of possibles.
def restart(board, List_Possible):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            board[r][c] = int(0)
    for it, l in enumerate(List_Possible):
        List_Possible[it - 1] = copy.deepcopy(TEST_LIST)

# This waits for a user-keyed value and returns the key value if 0 - 9
# This also prints to the top of the screen which cell locked until value entered and prompts the user for a number.
# When the user enters a value, it runs a separate function to interpret that keystroke
def wait_for_key():
    global user_good_input
    global user_value
    global gridx
    global gridy
    user_good_input = False
    while user_good_input == False:
        font = pygame.font.SysFont('courier', 15)
        label = font.render('What number is cell ('
                            + str(((int((gridy / SQUARESIZE)))))
                            + ', '
                            + str((int((gridx / SQUARESIZE))))
                            + ')', 1, YELLOW)
        cellx = (SQUARESIZE / 2)
        celly = (SQUARESIZE / 2)
        screen.blit(label, (int(cellx), int(celly)))
        pygame.display.update()
        w = pygame.event.wait()
        if w.type == pygame.QUIT:
            return pygame.K_ESCAPE
        if w.type == pygame.KEYDOWN:
            if w.key == pygame.K_0:
                user_value = 0
                user_good_input = True
            elif w.key == pygame.K_1:
                user_value = 1
                user_good_input = True
            elif w.key == pygame.K_2:
                user_value = 2
                user_good_input = True
            elif w.key == pygame.K_3:
                user_value = 3
                user_good_input = True
            elif w.key == pygame.K_4:
                user_value = 4
                user_good_input = True
            elif w.key == pygame.K_5:
                user_value = 5
                user_good_input = True
            elif w.key == pygame.K_6:
                user_value = 6
                user_good_input = True
            elif w.key == pygame.K_7:
                user_value = 7
                user_good_input = True
            elif w.key == pygame.K_8:
                user_value = 8
                user_good_input = True
            elif w.key == pygame.K_9:
                user_value = 9
                user_good_input = True
            else:
                pass
    value_entered(board)

# Setting up the board and visual rules for interface
board = create_board()
pygame.init()
SQUARESIZE = 50
width = (COLUMN_COUNT + 2) * SQUARESIZE
height = (ROW_COUNT + 2) * SQUARESIZE
size = (width, height)
wierd = False
screen = pygame.display.set_mode(size)

# This sets the stage. Calls various functions to make the board with randomly generated values.
# This also creates the list of possible answers.
draw_board(board)
pygame.display.update()
create_board()
generate_possibles()
squares_for_possibles()
start_values(board, List_Possible)
assign_squares()

# This creates the while loop for operating the game.
# There is a red dot and a yellow dot to visually suggest that the program pauses upon user click
# There is a green dot to imply where value input goes along with yellow text above the puzzle
# If there is a click on the puzzle board, then the puzzle waits for a 0-9 user input
# It then checks whether the puzzle is completed and valid.
# If the puzzle is completed and valid, the all_cells_entered functions indicator goes True and while loop breaks
# If the puzzle is complete and does not match the List of Possibles, then values are deleted.
# User is prompted to attempt the puzzle again with errors erased.
# After while loop breaks, the user is congratulated and board waits 5 seconds before closing itself.
while not all_cells_entered:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            pygame.draw.rect(screen, BLACK, (0, 0, SQUARESIZE, height))
            posx = event.pos[0]
            pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), 5)
            posy = event.pos[1]
            pygame.draw.circle(screen, YELLOW, (int(SQUARESIZE / 2), posy), 5)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] > SQUARESIZE and event.pos[0] < width - SQUARESIZE and event.pos[1] > SQUARESIZE and event.pos[1] < height - SQUARESIZE:
            pygame.mouse.get_pos()
            gridx = event.pos[0]
            gridy = event.pos[1]
            pygame.draw.circle(screen, GREEN, (gridx, gridy), 2)
            pygame.display.update()
            if board[(int((gridy/SQUARESIZE) - 1))][(int((gridx/SQUARESIZE) - 1))] == 0:
                wait_for_key()
                all_cells_check(board)
            else:
                pygame.time.wait(1000)
                draw_board(board)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mouse.get_pos()
            poss_toggle_x = event.pos[0]
            poss_toggle_y = event.pos[1]
            if int(SQUARESIZE) < poss_toggle_x < int(SQUARESIZE * 2) and int(height - (SQUARESIZE / 2)) < poss_toggle_y < int(height):
                toggle += 1
                poss_mod = toggle % 2
                button_for_possibles(List_Possible, board)

pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
pygame.draw.rect(screen, BLACK, (0, 0, SQUARESIZE, height))
pygame.display.update()
font = pygame.font.SysFont('courier', 15)
label = font.render('Congratulations, you won!', 1, YELLOW)
cellx = (SQUARESIZE / 2)
celly = (SQUARESIZE / 2)
screen.blit(label, (int(cellx), int(celly)))
pygame.display.update()
pygame.time.wait(5000)
print("Mission Success")
# Checklist for Sudoku Puzzle
'''
Draw the grid // Check
    Random number generation and placement // check
    Run possible solution checks // check
Determine where the user MOUSEDOWN // check
Determine what value the user entered // check
Enter the user-provided value into the board // check
    Populate the non-zero board values to the grid // check
    Error check for multiples in row/column/square // check
    Error check for possibles in list getting to blank // check
    Update possibles list in background // check
Build toggle buttons // check
    Check for puzzle validity // not done
    Show cell notes (this could print the possible remaining to the screen) // not done
Check for no more zeroes on board // check
    Run validity check // check
'''

