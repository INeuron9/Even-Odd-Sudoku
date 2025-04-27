# Even-Odd-Sudoku
Sudoku but a twist. Specific blocks are marked as even or odd.

**Project Overview**

Even-Odd Sudoku is an enhanced version of the traditional Sudoku puzzle game that introduces a unique twist: no two consecutive numbers in any row, column, or 3x3 subgrid can share the same parity (odd or even). The game is implemented using Python and the Pygame library for the user interface, while backtracking and constraint satisfaction algorithms solve the puzzle.

**Features**

Even-Odd Constraints: In addition to the standard Sudoku rules, consecutive numbers in rows, columns, and 3x3 grids must differ in parity (even vs. odd).

Puzzle Solver: A backtracking algorithm is used to automatically solve the puzzle while respecting both the usual Sudoku rules and the added even-odd constraint.

Interactive Interface: Built using Pygame, the game allows users to manually fill in the grid, receive hints, and solve the puzzle automatically.

Random Puzzle Generation: The game can generate puzzles with varying difficulty levels based on the random placement of numbers while respecting the even-odd constraint.

**Installation**

To run this project locally, ensure you have Python 3.x installed along with the required libraries. Follow the steps below to set up the project.


**Clone the repository:**

git clone https://github.com/INeuron9/even-odd-sudoku.git

**Install dependencies**

run the following command in cmd

py -m pip install -r requirements.txt


**Game Rules**

Standard Sudoku Rules: Fill a 9x9 grid with numbers from 1 to 9 such that:

Each number appears exactly once in each row.

Each number appears exactly once in each column.

Each number appears exactly once in each 3x3 subgrid.

Even-Odd Constraint: No two consecutive numbers in any row, column, or 3x3 subgrid can have the same parity (i.e., one must be odd and the other even).

Objective: Solve the puzzle while respecting both the Sudoku and the even-odd constraints.
