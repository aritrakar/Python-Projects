from time import perf_counter
import math
from typing import List, Any
from random import random
import copy
# from numba import jit

# Define types for convenience
BoardType = List[List[int]]
StateType = List[List[str]]

RUNS = 25
DIGITS = '123456789'

# Boards
BOARD_EASY = [
    [0,5,8,0,6,2,1,0,0],
    [0,0,2,7,0,0,4,0,0],
    [0,6,7,9,0,1,2,5,0],
    [0,8,6,3,4,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,7,6,8,9,0],
    [0,2,9,6,0,8,7,4,0],
    [0,0,3,0,0,4,9,0,0],
    [0,0,5,2,9,0,3,8,0]
]

BOARD_MEDIUM = [
    [8,3,0,6,0,0,0,0,7],
    [0,0,7,0,2,0,0,5,0],
    [0,2,1,0,0,9,0,8,0],
    [6,0,0,0,8,0,0,0,9],
    [0,0,0,4,6,5,0,0,0],
    [3,0,0,0,9,0,0,0,2],
    [0,8,0,2,0,0,3,9,0],
    [0,5,0,0,4,0,2,0,0],
    [2,0,0,0,0,8,0,1,6]
]

BOARD_HARD = [
    [1,0,0,0,3,0,0,0,0],
    [0,6,2,0,0,0,0,0,0],
    [0,0,0,7,0,2,8,0,4],
    [0,7,0,1,4,0,0,0,2],
    [0,4,0,0,0,0,0,9,0],
    [8,0,0,0,5,6,0,7,0],
    [6,0,9,8,0,7,0,0,0],
    [0,0,0,0,0,0,2,1,0],
    [0,0,0,0,6,0,0,0,9],
]

BOARD_EVIL = [
    [0,1,0,0,0,0,0,0,6],
    [9,0,0,2,0,0,0,0,0],
    [7,3,2,0,4,0,0,1,0],
    [0,4,8,3,0,0,0,0,2],
    [0,0,0,0,0,0,0,0,0],
    [3,0,0,0,0,4,6,7,0],
    [0,9,0,0,3,0,5,6,8],
    [0,0,0,0,0,2,0,0,1],
    [6,0,0,0,0,0,0,3,0]
]

BOARDS = [BOARD_EASY, BOARD_MEDIUM, BOARD_HARD, BOARD_EVIL]
BOARDS2 = copy.deepcopy(BOARDS)
BOARDS3 = copy.deepcopy(BOARDS)

# To store the number of nodes
# TODO: Make this part of the function to reduce overhead
nodes = 0

def mean(arr):
    assert(len(arr) > 0)
    '''Returns the mean of `arr`.'''
    return sum(arr) / len(arr)

def std(arr):
    '''Returns both the mean and standard deviation.'''
    arr_mean = mean(arr)
    return (arr_mean, math.sqrt(sum(pow(x-arr_mean,2) for x in arr) / len(arr)))

def get_random_item(arr):
    '''Returns a random item from `arr`.'''
    return arr[int(math.floor(random() * len(arr)))]

def print_board(b: Any):
    '''Prints a 9x9 board.'''
    for r in range(9):
        temp = ""
        for c in range(9):
            temp += str(b[r][c]) + " "
        print(temp)

def init_states() -> StateType:
    '''Initializes grid of states such that all states start with `DIGITS`.'''
    states = []
    for _ in range(9):
        temp = []
        for _ in range(9):
            temp.append(DIGITS)
        states.append(temp)
    return states

def assign(states: StateType, row: int, col: int, value: int):
    '''Assigns `value` to `state[row][col]` and removes it from `row`,
    `col`, and the corresponding box.'''
    value = str(value)
    
    # Remove the same value from other unassigned cells
    # in the same:
    # Row
    for c in range(9):
        if (value in states[row][c]):
            states[row][c] = states[row][c].replace(value, "")

    # Column
    for r in range(9):
        if (value in states[r][col]):
            states[r][col] = states[r][col].replace(value, "")

    # Box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if (value in states[box_row + i][box_col + j]):
                states[box_row + i][box_col + j] = states[box_row + i][box_col + j].replace(value, "")

    # Don't forget to assign the value!
    states[row][col] = value

def is_valid(board: BoardType, row: int, col: int, num: int):
    '''Checks for duplicates if `num` were inserted at `(row, col)` in `board`.'''
    # Check row
    for i in range(9):
        if board[row][i] == num:
            return False

    # Check column
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check 3x3 box
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def get_empty_cells(board: BoardType) -> BoardType:
    '''Returns a list of empty cells in `board`.'''
    empty_cells = []
    for r in range(9):
        for c in range(9):
            if (board[r][c] == 0):
                empty_cells.append([r, c])
    return empty_cells

def backtracking(board: BoardType):
    '''Solve `board` using backtracking with random variable and value ordering.'''
    # Update number of nodes
    global nodes
    nodes += 1

    empty_cells = get_empty_cells(board)

    # If there are no empty cells, then the puzzle is complete
    if (len(empty_cells) == 0):
        return True

    # Otherwise, find a random empty cell
    row, col = get_random_item(empty_cells)

    domain = list(range(1, 10))

    while (len(domain) > 0):
        # Get a random value from the domain
        value = get_random_item(domain)

        # Remove the value from the domain because we will have traversed it
        domain.remove(value)

        # Check constraints
        if is_valid(board, row, col, value):
            board[row][col] = value

            if backtracking(board):
                return True

            board[row][col] = 0

    return False

def get_remaining_values(board: BoardType, row: int, col: int):
    '''Gets the list of possible values for `board[row][col]`.'''
    domain = set(range(1, 10))

    # Collect values in the same row and column
    row_vals = set(board[row])
    col_vals = set([board[r][col] for r in range(9)])

    # Collect values in the same box
    cell_vals = []
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            cell_vals.append(board[start_row + i][start_col + j])

    # Collect all the values
    all_vals = row_vals.union(col_vals).union(cell_vals)
    
    domain = domain.difference(all_vals)

    return list(domain)

def forward_check(row: int, col: int, value, states: StateType):
    pass

# @jit(target_backend='cuda')
def btfc(board: BoardType):
    '''Solve `board` with backtracking combined with forward
    checking and random variable and value ordering.'''
    
    # Update number of nodes
    global nodes
    nodes += 1

    empty_cells = get_empty_cells(board)

    if (len(empty_cells) == 0):
        return True
    
    row, col = get_random_item(empty_cells)

    values = get_remaining_values(board, row, col)

    # for num in values:
    while (len(values) > 0):
        num = get_random_item(values)
        values.remove(num)

        if is_valid(board, row, col, num):
            board[row][col] = num

            if btfc(board):
                return True

            board[row][col] = 0

    return False

# @jit(target_backend='cuda')
def btfch(board):
    # Update number of nodes
    global nodes
    nodes += 1
    
    chosen_cell = [-1, -1]

    # Get all empty cells
    empty_cells = get_empty_cells(board)

    if (len(empty_cells) == 0):
        return True

    # Find the most constrained cell
    states = get_all_remaining_values(board)
    min_constraint = min(list(map(lambda cell: len(states[cell[0]][cell[1]]), empty_cells)))
    most_constrained_cells = []
    for cell in empty_cells:
        r, c = cell
        if (len(states[r][c]) == min_constraint):
            most_constrained_cells.append(cell)

    # Check for tie
    if (len(most_constrained_cells) == 1):
        # No tie, so only one cell
        chosen_cell = most_constrained_cells[0]
    else:
        # There is a tie. Move on to next heuristic.

        # Find the most constraining cell
        most_constraining_cells = []
        degrees = list(map(lambda cell: get_degree(board, cell[0], cell[1]), most_constrained_cells))
        max_degree = max(degrees)

        for i in range(len(most_constrained_cells)):
            if (degrees[i] == max_degree):
                most_constraining_cells.append(most_constrained_cells[i])

        # If there's yet another tie, choose a random cell
        if (len(most_constraining_cells) == 1):
            chosen_cell = most_constraining_cells[0]
        else:
            chosen_cell = get_random_item(most_constraining_cells)

    row, col = chosen_cell

    # Will this ever be a case? If it is, it's a wrong configuration
    # if (row == -1 or col == -1):
    #     return False

    # Now to find the least constraining value
    values = list(states[row][col])

    while (len(values) > 0):
        lcv_list = get_lcv(values, row, col, states)

        # Choose the least constraining value, and remove it from the list
        num = values[lcv_list.index(min(lcv_list))]
        values.remove(num)

        if is_valid(board, row, col, num):
            board[row][col] = num

            if btfch(board):
                return True

            board[row][col] = 0

    return False

def get_all_remaining_values(board: BoardType):
    '''Get the grid of possible values of each cell in `board`.'''
    # Initialize the states
    states = init_states()

    # For each value in `board`, assign() will eliminate the possibilities
    # of other cells sharing the row, column, and box are the current cell.
    for r in range(9):
        for c in range(9):
            if (board[r][c] != 0):
                assign(states, r, c, str(board[r][c]))

    return states

def get_degree(board: BoardType, row: int, col: int):
    degree = 0

    for c in range(9):
        if (c == col):
            continue                
        if (board[row][c] == 0):
            degree += 1
     
    for r in range(9):
        if (r == row):
            continue
        if (board[r][col] == 0):
            degree += 1

    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):            
            if [box_row + i, box_col + j] == [row, col]:
                continue        
            if board[box_row + i][box_col + j] == 0:
                degree += 1

    return degree

def get_lcv(values, row: int, col: int, states: StateType):
    '''Counts the number of times a value appears in constrained cells.'''
    lcv_list = []
    
    for value in values:
        count = 0

        # Row
        for c in range(9):
            if ((c == col) and (value in states[row][c])):
                count += 1
        
        # Column
        for r in range(9):
            if ((r != row) and (value in states[r][col])):
                count += 1

        # Box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if (([box_row + i, box_col + j] == [row, col]) and
                    (value in states[box_row + i][box_col + j])):
                    count += 1

        lcv_list.append(count)

    return lcv_list


def run_multiple_times(board, func):
    '''Run `func` on `board` for `RUNS` iterations.'''
    global nodes
    times = []
    numNodes = []

    for _ in range(RUNS):
        # Extra safety
        if (nodes != 0):
            nodes = 0

        start_time = perf_counter()
        result = func(board)
        end_time = perf_counter()

        if (result):
            # CAREFUL! Converting to ms from s
            times.append((end_time - start_time) * 1000)
            numNodes.append(nodes)

        # Reset nodes
        nodes = 0

    times_mean, times_std = std(times)
    nodes_mean, nodes_std = std(numNodes)

    print("Time taken: ", times_mean, " +- ", times_std, "ms")
    print("Nodes: ", nodes_mean, " +- ", nodes_std)

def run_all(boards, func):
    '''Runs `func` on boards in `boards` which contains boards of all difficulties.'''
    print("Getting statistics for ", func.__name__)

    levels = ["Easy", "Medium", "Hard", "Evil"]
    for i, board in enumerate(boards):
        print(levels[i])
        run_multiple_times(board, func)
        print("-------------------------------------------------------------------")


if __name__ == "__main__":
    run_all(BOARDS, btfch)
    print("---------------------------------------")
    run_all(BOARDS2, btfc)
    print("---------------------------------------")
    # WARNING: Takes a really long time (hours)!
    run_all(BOARDS3, backtracking)
