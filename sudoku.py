import tkinter as tk
from tkinter import ttk, messagebox
import random
import copy

CELL = 60

CORRECT = "#2563eb"  
WRONG   = "#dc2626"   
FIXED   = "#111827"
USER    = "#4f46e5"


class ModernSudoku:
    def __init__(self, root):
        root.title("Modern PySudoku")
        root.resizable(False, False)

        self.board = [[0]*9 for _ in range(9)]
        self.solution = None
        self.fixed = [[False]*9 for _ in range(9)]
        self.selected = None
        self.finished = False

        self.canvas = tk.Canvas(root, width=540, height=540, bg="white")
        self.canvas.pack(padx=20, pady=20)

        self.draw_grid()
        self.canvas.bind("<Button-1>", self.select_cell)
        root.bind("<Key>", self.key_input)

        panel = ttk.Frame(root)
        panel.pack()

        ttk.Button(panel, text="Generate", command=self.generate).grid(row=0, column=0, padx=5)
        ttk.Button(panel, text="Solve", command=self.solve).grid(row=0, column=1, padx=5)
        ttk.Button(panel, text="Finish", command=self.finish).grid(row=0, column=2, padx=5)
        ttk.Button(panel, text="Clear", command=self.clear).grid(row=0, column=3, padx=5)


    def draw_grid(self):
        for i in range(10):
            w = 3 if i % 3 == 0 else 1
            self.canvas.create_line(0, i*CELL, 540, i*CELL, width=w)
            self.canvas.create_line(i*CELL, 0, i*CELL, 540, width=w)

    def draw_numbers(self):
        self.canvas.delete("num")
        for r in range(9):
            for c in range(9):
                n = self.board[r][c]
                if n != 0:
                    if self.fixed[r][c]:
                        color = FIXED
                    elif self.finished:
                        color = CORRECT if n == self.solution[r][c] else WRONG
                    else:
                        color = USER

                    self.canvas.create_text(
                        c*CELL + 30, r*CELL + 30,
                        text=n, font=("Segoe UI", 18, "bold"),
                        fill=color, tags="num"
                    )


    def select_cell(self, e):
        if self.finished:
            return
        r, c = e.y // CELL, e.x // CELL
        if 0 <= r < 9 and 0 <= c < 9 and not self.fixed[r][c]:
            self.selected = (r, c)

    def key_input(self, e):
        if not self.selected or self.finished:
            return
        if e.char in "123456789":
            r, c = self.selected
            self.board[r][c] = int(e.char)
            self.draw_numbers()


    def finish(self):
        for row in self.board:
            if 0 in row:
                messagebox.showwarning("Incomplete", "Fill all cells first!")
                return

        self.finished = True
        self.draw_numbers()

        if self.board == self.solution:
            messagebox.showinfo("Success", "🎉 All answers are correct!")
        else:
            messagebox.showerror("Wrong", "❌ Mistakes shown in RED")

    
    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    return r, c
        return None

    def is_safe(self, r, c, n):
        if n in self.board[r]:
            return False
        if n in [self.board[i][c] for i in range(9)]:
            return False

        sr, sc = (r//3)*3, (c//3)*3
        for i in range(sr, sr+3):
            for j in range(sc, sc+3):
                if self.board[i][j] == n:
                    return False
        return True

    def solve_board(self):
        pos = self.find_empty()
        if not pos:
            return True
        r, c = pos

        for n in range(1, 10):
            if self.is_safe(r, c, n):
                self.board[r][c] = n
                if self.solve_board():
                    return True
                self.board[r][c] = 0
        return False

    def solve(self):
        temp = copy.deepcopy(self.board)

        if not self.solve_board():
            messagebox.showerror("Error", "No solution exists!")
            self.board = temp
            return

        self.solution = copy.deepcopy(self.board)
        self.finished = True
        self.draw_numbers()


    def generate(self):
        self.clear()

    
        nums = list(range(1, 10))
        random.shuffle(nums)
        self.board[0] = nums

        self.solve_board()
        self.solution = copy.deepcopy(self.board)

    
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)

        for i in range(50):
            r, c = cells[i]
            self.board[r][c] = 0

        for r in range(9):
            for c in range(9):
                self.fixed[r][c] = self.board[r][c] != 0

        self.draw_numbers()

    
    def clear(self):
        self.board = [[0]*9 for _ in range(9)]
        self.fixed = [[False]*9 for _ in range(9)]
        self.solution = None
        self.finished = False
        self.selected = None
        self.canvas.delete("num")


if __name__ == "__main__":
    root = tk.Tk()
    ModernSudoku(root)
    root.mainloop()
