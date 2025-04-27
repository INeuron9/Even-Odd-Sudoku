# Even-Odd-Sudoku
Sudoku but a twist. Specific blocks are marked as even or odd.

**Project Overview**

Even-Odd Sudoku is an enhanced version of the traditional Sudoku puzzle game that introduces a unique twist: no two consecutive numbers in any row, column, or 3x3 subgrid can share the same parity (odd or even). The game is implemented using Python and the Pygame library for the user interface, while backtracking and constraint satisfaction algorithms solve the puzzle.

**Features**

Even-Odd Constraints: In addition to the standard Sudoku rules, consecutive numbers in rows, columns, and 3x3 grids must differ in parity (even vs. odd).

Puzzle Solver: A backtracking algorithm is used to automatically solve the puzzle while respecting both the usual Sudoku rules and the added even-odd constraint.

Interactive Interface: Built using Pygame, the game allows users to manually fill in the grid, receive hints, and solve the puzzle automatically.

Random Puzzle Generation: The game can generate puzzles with varying difficulty levels based on the random placement of numbers while respecting the even-odd constraint.

