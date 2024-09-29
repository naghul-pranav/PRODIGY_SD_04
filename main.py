import tkinter as tk
from tkinter import messagebox

# Backtracking Sudoku Solver
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(board):
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True  # Solved
    row, col = empty_cell
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0  # Backtrack
    return False

def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def is_board_valid(board):
    for i in range(9):
        row = [num for num in board[i] if num != 0]
        if len(row) != len(set(row)):
            return False
        col = [board[j][i] for j in range(9) if board[j][i] != 0]
        if len(col) != len(set(col)):
            return False

    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            subgrid = []
            for i in range(3):
                for j in range(3):
                    num = board[row + i][col + j]
                    if num != 0:
                        subgrid.append(num)
            if len(subgrid) != len(set(subgrid)):
                return False
    return True

class SudokuSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.geometry("400x500")
        
        # Create a frame for the grid to hold the entire 9x9 grid
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(pady=20)

        # Create a 9x9 grid of Entry widgets for Sudoku input
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_grid()

        # Solve and Reset buttons
        self.btn_solve = tk.Button(self.root, text="Solve Sudoku", command=self.solve)
        self.btn_solve.pack(pady=10)
        
        self.btn_reset = tk.Button(self.root, text="Reset Grid", command=self.reset_grid)
        self.btn_reset.pack(pady=10)

    def create_grid(self):
        # Create the 9x9 grid layout with 3x3 subgrid borders
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.grid_frame, width=2, font=('Arial', 18), justify='center', bd=3)

                # Add thicker borders between 3x3 subgrids
                if row % 3 == 0 and row != 0:
                    entry.grid(row=row, column=col, padx=1, pady=(5, 1))  # Thicker horizontal border
                else:
                    entry.grid(row=row, column=col, padx=1, pady=1)

                if col % 3 == 0 and col != 0:
                    entry.grid_configure(padx=(5, 1))  # Thicker vertical border

                # Store the entry widget for access later
                self.entries[row][col] = entry

    def solve(self):
        board = self.get_board_from_entries()

        if not is_board_valid(board):
            messagebox.showerror("Sudoku Solver", "The input Sudoku puzzle is invalid (duplicate numbers). Please correct it.")
            return
        
        if solve_sudoku(board):
            self.display_solution(board)
        else:
            messagebox.showerror("Sudoku Solver", "No solution exists for this Sudoku puzzle!")

    def get_board_from_entries(self):
        board = []
        for row in range(9):
            current_row = []
            for col in range(9):
                val = self.entries[row][col].get()
                if val.isdigit():
                    current_row.append(int(val))
                else:
                    current_row.append(0)
            board.append(current_row)
        return board

    def display_solution(self, board):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                self.entries[row][col].insert(0, str(board[row][col]))

    def reset_grid(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)

# Main Window
root = tk.Tk()
app = SudokuSolverApp(root)
root.mainloop()
