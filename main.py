import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe")
        self.geometry("400x500")
        self.configure(bg="#2c2c2c")

        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the position of the window to center it on the screen
        x = (screen_width - 400) // 2
        y = (screen_height - 500) // 2

        self.geometry(f"400x500+{x}+{y}")

        self.start_frame = StartPage(self)
        self.game_frame = GamePage(self)

        self.start_frame.pack()
        self.game_frame.pack_forget()

    def show_game_frame(self, mode):
        self.start_frame.pack_forget()
        self.game_frame.set_mode(mode)
        self.game_frame.pack()

    def reset_game(self):
        self.game_frame.reset_game()
        self.game_frame.pack_forget()
        self.start_frame.pack()


class StartPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2c2c2c")
        self.parent = parent
        label = tk.Label(self, text="Tic Tac Toe", font=("Helvetica", 28), bg="#2c2c2c", fg="#ffffff")
        label.pack(pady=(30, 10))

        button_friend = tk.Button(self, text="Play against Friend", font=("Helvetica", 14),
                                   command=lambda: self.parent.show_game_frame("friend"), bg="#f57c00", fg="#ffffff", padx=10, pady=5)
        button_friend.pack(pady=10)

        button_computer = tk.Button(self, text="Play against Computer", font=("Helvetica", 14),
                                     command=lambda: self.parent.show_game_frame("computer"), bg="#f57c00", fg="#ffffff", padx=10, pady=5)
        button_computer.pack(pady=10)


class GamePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2c2c2c")
        self.parent = parent
        self.mode = None

        self.current_player = "X"
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

    def set_mode(self, mode):
        self.mode = mode

    def create_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self, text=" ", font=("Helvetica", 20), width=6, height=3,
                                                command=lambda row=i, col=j: self.make_move(row, col), bg="#f57c00", fg="#ffffff")
                self.buttons[i][j].grid(row=i, column=j, padx=2, pady=2)

    def make_move(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, state="disabled", disabledforeground="#424242")
            if self.check_winner():
                messagebox.showinfo("Winner", f"Player {self.current_player} wins!")
                self.parent.reset_game()
            elif self.check_tie():
                messagebox.showinfo("Tie", "It's a tie!")
                self.parent.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.mode == "computer" and self.current_player == "O":
                    self.computer_move()

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return True
        return False

    def check_tie(self):
        return all(cell != " " for row in self.board for cell in row)

    def reset_game(self):
        self.current_player = "X"
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ", state="normal")

    def computer_move(self):
        # Check if computer can win in the next move
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = "O"
                    if self.check_winner():
                        self.buttons[i][j].config(text="O", state="disabled", disabledforeground="#424242")
                        messagebox.showinfo("Winner", "Computer wins!")
                        self.parent.reset_game()
                        return
                    self.board[i][j] = " "

        # Check if user can win in the next move, and block them
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = "X"
                    if self.check_winner():
                        self.board[i][j] = "O"
                        self.buttons[i][j].config(text="O", state="disabled", disabledforeground="#424242")
                        self.current_player = "X"
                        return
                    self.board[i][j] = " "

        # Choose a random empty cell
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = "O"
            self.buttons[row][col].config(text="O", state="disabled", disabledforeground="#424242")
            if self.check_winner():
                messagebox.showinfo("Winner", "Computer wins!")
                self.parent.reset_game()
            elif self.check_tie():
                messagebox.showinfo("Tie", "It's a tie!")
                self.parent.reset_game()
            else:
                self.current_player = "X"

if __name__ == "__main__":
    app = TicTacToe()
    app.mainloop()
