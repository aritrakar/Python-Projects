# Sudoku Solver

This repository contains code for a sudoku solver, illustrating different concepts of search algorithms. The sudoku problem is formulated as a constraint satisfaction problem.
- **Variables:** $V_1, V_2, \ldots, V_{81}$ representing each of the 81 cells.

  Alternatively, we could define the variables are $V_{ij}, i,j \in \{1, \ldots, 9\}$ where $i, j$ represent the rows and columns respectively.

- **Domain:** $\{1, \ldots, 9\}$ the numbers 1 through 9 represent the value of that cell.
  Note: 0 is used to represent the empty cell, so technically it's not a part of the domain.

- **Constraints:**
    1. Each row contains integers from 1 to 9 without repetitions. There are 9 such constraints because there are 9 rows.
    2. Each column contains integers from 1 to 9 without repetitions. There are 9 such constraints because there are 9 columns.
    3. Each box ($3 \times 3$ unit) contains integers from 1 to 9 without repetitions. There are 9 such constraints because there are 9 boxes.

**Notes about the algorithms and experiments:**
- Each algorithm was run on each puzzle at least 25 times and the runtime and number of nodes expanded were noted for calculation.
- The control model employs only backtracking with randomized variable and value assignment.

  Interestingly, when executing the code with sequential cell and value assignment, I found that the outcome was similar to backtracking with forward checking because the search space was more constrained.
- The first improved model employs both backtracking and forward checking. It showed a significant improvement over the control model even with the random variable and value assignment.
- The final model employed backtracking (again with random variable and value assignment), forward checking, and 3 heuristics. The heuristics employed were:
  - Least constrained value
  - Most constrained variable
  - Most constraining variable
- There are 4 puzzles of increasing difficulty: Easy, Medium, Hard, and Evil.

### TODOs
1. Insert table of runtimes and nodes.
2. Improve runtimes using Numba.
3. Upload C++ version.
