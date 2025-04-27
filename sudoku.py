import pygame
import sys
import random
import time
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
GRID_SIZE = 500
CELL_SIZE = GRID_SIZE // 9
MARGIN = (WINDOW_WIDTH - GRID_SIZE) // 2

# Color Palette
WHITE = (255, 255, 255)
BLACK = (40, 40, 40)
LIGHT_GRAY = (240, 240, 240)
MEDIUM_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (70, 130, 180)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
RED = (220, 20, 60)
GREEN = (34, 139, 34)
LIGHT_GREEN = (144, 238, 144)
PURPLE = (147, 112, 219)
EVEN_OUTLINE = (100, 149, 237)  # Cornflower blue
ODD_OUTLINE = (255, 182, 193)   # Light pink
BACKGROUND = (249, 246, 239)     # Soft beige background

# Set up window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Even-Odd Sudoku by K224708,K224792,K224779)')
font_large = pygame.font.SysFont('Arial', 36, bold=True)
font_medium = pygame.font.SysFont('Arial', 28)
font_small = pygame.font.SysFont('Arial', 20)
font_tiny = pygame.font.SysFont('Arial', 16)

class SudokuGame:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.even_cells = set()
        self.odd_cells = set()
        self.selected = None
        self.start_time = 0
        self.elapsed_time = 0
        self.game_over = False
        self.solving = False
        self.hints_used = 0
        self.generate_puzzle()
        
    def generate_puzzle(self):
        """Generate a new Sudoku puzzle with even-odd constraints"""
        self.solution = self.generate_solution()
        for i in range(9):
            for j in range(9):
                self.board[i][j] = self.solution[i][j]
        
        # Determine which cells will be clues (pre-filled)
        clue_cells = set()
        for i in range(9):
            for j in range(9):
                if random.random() < 0.25:  # 25% chance to be a clue
                    clue_cells.add((i, j))
        
        self.even_cells = set()
        self.odd_cells = set()
        
        # Add even-odd constraints to some non-clue cells
        for i in range(9):
            for j in range(9):
                if (i, j) not in clue_cells and random.random() < 0.15:
                    num = self.board[i][j]
                    if num % 2 == 0:
                        self.even_cells.add((i, j))
                    else:
                        self.odd_cells.add((i, j))
        
        # Empty some cells to create the puzzle
        empty_cells = random.randint(40, 50)
        cells = [(i, j) for i in range(9) for j in range(9) if (i, j) not in clue_cells]
        random.shuffle(cells)
        
        for i, j in cells[:empty_cells]:
            self.board[i][j] = 0
        
        self.start_time = time.time()
        self.game_over = False
        self.hints_used = 0
    
    def generate_solution(self):
        """Generate a valid Sudoku solution using pattern method"""
        base = 3
        side = base * base
        
        def pattern(r, c): return (base * (r % base) + r // base + c) % side
        
        from random import sample
        def shuffle(s): return sample(s, len(s))
        
        r_base = range(base)
        rows = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)]
        cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]
        nums = shuffle(range(1, base * base + 1))
        
        board = [[nums[pattern(r, c)] for c in cols] for r in rows]
        
        return board

    def is_valid(self, row, col, num):
        """Check if a number can be placed in a cell"""
        if num == 0:
            return True
            
        # Check row and column
        for i in range(9):
            if self.board[row][i] == num and i != col:
                return False
            if self.board[i][col] == num and i != row:
                return False
                
        # Check 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num and (i != row or j != col):
                    return False
                    
        # Check even-odd constraints
        if (row, col) in self.even_cells and num % 2 != 0:
            return False
        if (row, col) in self.odd_cells and num % 2 == 0:
            return False
            
        return True

    def solve_board(self):
        """Solve the board recursively with visualization"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(i, j, num):
                            self.board[i][j] = num
                            self.selected = (i, j)
                            self.draw()
                            pygame.display.update()
                            pygame.time.delay(30)  # Animation speed
                            if self.solve_board():
                                return True
                            self.board[i][j] = 0
                            self.draw()
                            pygame.display.update()
                            pygame.time.delay(30)
                    return False
        return True

    def get_hint(self):
        """Provide a hint by filling in a random empty cell"""
        empty_cells = [(i, j) for i in range(9) for j in range(9) if self.board[i][j] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = self.solution[row][col]
            self.hints_used += 1
            return True
        return False

    def check_completion(self):
        """Check if the board is completely and correctly filled"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 or not self.is_valid(i, j, self.board[i][j]):
                    return False
        return True

    def draw(self):
        """Draw the game interface"""
        window.fill(BACKGROUND)
        
        # Draw title
        title = font_large.render('Even-Odd Sudoku', True, DARK_BLUE)
        window.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 15))
        
        # Draw timer
        if not self.game_over:
            self.elapsed_time = int(time.time() - self.start_time)
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        time_text = font_small.render(f'Time: {minutes:02d}:{seconds:02d}', True, BLACK)
        window.blit(time_text, (WINDOW_WIDTH - 130, 25))
        
        # Draw grid background
        grid_rect = pygame.Rect(MARGIN, MARGIN + 60, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(window, WHITE, grid_rect)
        
        # Draw even-odd constraints first (so numbers appear on top)
        for i in range(9):
            for j in range(9):
                cell_rect = pygame.Rect(MARGIN + j * CELL_SIZE, MARGIN + 60 + i * CELL_SIZE, 
                                      CELL_SIZE, CELL_SIZE)
                if (i, j) in self.even_cells and self.board[i][j] == 0:
                    pygame.draw.rect(window, EVEN_OUTLINE, cell_rect, 3)
                elif (i, j) in self.odd_cells and self.board[i][j] == 0:
                    pygame.draw.rect(window, ODD_OUTLINE, cell_rect, 3)
        
        # Draw grid lines
        for i in range(10):
            line_width = 4 if i % 3 == 0 else 2
            # Horizontal lines
            pygame.draw.line(window, BLACK, 
                           (MARGIN, MARGIN + 60 + i * CELL_SIZE), 
                           (MARGIN + GRID_SIZE, MARGIN + 60 + i * CELL_SIZE), 
                           line_width)
            # Vertical lines
            pygame.draw.line(window, BLACK, 
                           (MARGIN + i * CELL_SIZE, MARGIN + 60), 
                           (MARGIN + i * CELL_SIZE, MARGIN + 60 + GRID_SIZE), 
                           line_width)
        
        # Draw numbers
        for i in range(9):
            for j in range(9):
                cell_rect = pygame.Rect(MARGIN + j * CELL_SIZE, MARGIN + 60 + i * CELL_SIZE, 
                                       CELL_SIZE, CELL_SIZE)
                
                # Highlight selected cell
                if self.selected == (i, j):
                    pygame.draw.rect(window, LIGHT_BLUE, cell_rect)
                
                num = self.board[i][j]
                if num != 0:
                    # Determine color based on correctness (for user inputs)
                    color = DARK_BLUE if self.board[i][j] == self.solution[i][j] else RED
                    num_text = font_medium.render(str(num), True, color)
                    window.blit(num_text, 
                              (MARGIN + j * CELL_SIZE + CELL_SIZE // 2 - num_text.get_width() // 2, 
                               MARGIN + 60 + i * CELL_SIZE + CELL_SIZE // 2 - num_text.get_height() // 2))

        # Draw buttons
        button_height = 40
        button_width = 100
        button_y = WINDOW_HEIGHT - 80
        
        # Solve button
        solve_rect = pygame.Rect(MARGIN, button_y, button_width, button_height)
        pygame.draw.rect(window, GREEN if not self.game_over else MEDIUM_GRAY, solve_rect, border_radius=5)
        solve_text = font_small.render('Solve', True, WHITE)
        window.blit(solve_text, (solve_rect.centerx - solve_text.get_width() // 2, 
                                solve_rect.centery - solve_text.get_height() // 2))
        
        # Hint button
        hint_rect = pygame.Rect(MARGIN + button_width + 10, button_y, button_width, button_height)
        pygame.draw.rect(window, PURPLE if not self.game_over else MEDIUM_GRAY, hint_rect, border_radius=5)
        hint_text = font_small.render('Hint', True, WHITE)
        window.blit(hint_text, (hint_rect.centerx - hint_text.get_width() // 2, 
                              hint_rect.centery - hint_text.get_height() // 2))
        
        # Reset button
        reset_rect = pygame.Rect(MARGIN + 2*(button_width + 10), button_y, button_width, button_height)
        pygame.draw.rect(window, BLUE, reset_rect, border_radius=5)
        reset_text = font_small.render('New Game', True, WHITE)
        window.blit(reset_text, (reset_rect.centerx - reset_text.get_width() // 2, 
                               reset_rect.centery - reset_text.get_height() // 2))
        
        # Hints used counter
        hints_text = font_tiny.render(f'Hints used: {self.hints_used}', True, DARK_GRAY)
        window.blit(hints_text, (WINDOW_WIDTH - MARGIN - hints_text.get_width(), button_y + 10))
        
        # Game over message
        if self.check_completion() and not self.game_over:
            self.game_over = True
            completion_text = font_medium.render('Puzzle Completed!', True, GREEN)
            window.blit(completion_text, (WINDOW_WIDTH // 2 - completion_text.get_width() // 2, 
                                       WINDOW_HEIGHT - 120))

        pygame.display.update()

    def reset_game(self):
        """Reset the game with a new puzzle"""
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.selected = None
        self.game_over = False
        self.solving = False
        self.hints_used = 0
        self.generate_puzzle()

def main():
    """Main game loop"""
    game = SudokuGame()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                
                # Check if a cell was clicked
                if MARGIN <= x < MARGIN + GRID_SIZE and MARGIN + 60 <= y < MARGIN + 60 + GRID_SIZE:
                    col = (x - MARGIN) // CELL_SIZE
                    row = (y - MARGIN - 60) // CELL_SIZE
                    game.selected = (row, col)
                
                # Check if buttons were clicked
                button_height = 40
                button_width = 100
                button_y = WINDOW_HEIGHT - 80
                
                # Solve button
                solve_rect = pygame.Rect(MARGIN, button_y, button_width, button_height)
                if solve_rect.collidepoint(x, y) and not game.game_over:
                    game.solving = True
                    game.solve_board()
                    game.game_over = True
                
                # Hint button
                hint_rect = pygame.Rect(MARGIN + button_width + 10, button_y, button_width, button_height)
                if hint_rect.collidepoint(x, y) and not game.game_over:
                    game.get_hint()
                
                # Reset button
                reset_rect = pygame.Rect(MARGIN + 2*(button_width + 10), button_y, button_width, button_height)
                if reset_rect.collidepoint(x, y):
                    game.reset_game()

            if event.type == KEYDOWN and game.selected and not game.game_over:
                row, col = game.selected
                if event.key in [K_1, K_KP1]: num = 1
                elif event.key in [K_2, K_KP2]: num = 2
                elif event.key in [K_3, K_KP3]: num = 3
                elif event.key in [K_4, K_KP4]: num = 4
                elif event.key in [K_5, K_KP5]: num = 5
                elif event.key in [K_6, K_KP6]: num = 6
                elif event.key in [K_7, K_KP7]: num = 7
                elif event.key in [K_8, K_KP8]: num = 8
                elif event.key in [K_9, K_KP9]: num = 9
                elif event.key in [K_BACKSPACE, K_DELETE, K_0, K_KP0]: num = 0
                else: num = None
                
                if num is not None and game.is_valid(row, col, num):
                    game.board[row][col] = num
                    if game.check_completion():
                        game.game_over = True
        
        game.draw()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
