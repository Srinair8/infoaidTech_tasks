import tkinter as tk
import random
from tkinter import messagebox
from tkinter import ttk

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("400x400")

        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.max_attempts = 10

        self.frame = tk.Frame(root, bg="lightblue")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.frame, text="Welcome to the Number Guessing Game!", bg="lightblue", font=("Arial", 14))
        self.label.pack(pady=10)

        self.name_label = tk.Label(self.frame, text="What's your name?", bg="lightblue", font=("Arial", 12))
        self.name_label.pack()

        self.name_entry = tk.Entry(self.frame, font=("Arial", 12))
        self.name_entry.pack()

        self.start_button = tk.Button(self.frame, text="Start Game", command=self.start_game, font=("Arial", 12))
        self.start_button.pack()

        self.quit_button = tk.Button(self.frame, text="Quit Game", command=self.root.destroy, font=("Arial", 12)) 
        self.quit_button.pack()

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.frame, variable=self.progress_var, maximum=self.max_attempts, mode="determinate")
        self.progress_bar.pack(fill=tk.X, padx=20, pady=10)

    def start_game(self):
        self.player_name = self.name_entry.get()
        if not self.player_name:
            messagebox.showinfo("Error", "Please enter your name.")
            return

        self.label.config(text=f"Hello, {self.player_name}! Here are the rules:\nI will generate a random number between 1 and 100,and you have 10 attempts to guess it.\nI will give you feedback on whether your guess is too high or too low. Let's get started!")

        self.name_label.pack_forget()
        self.name_entry.pack_forget()
        self.start_button.pack_forget()
        self.quit_button.pack_forget()

        self.guess_label = tk.Label(self.frame, text="Guess the number (1-100):", bg="lightblue", font=("Arial", 12))
        self.guess_label.pack()

        self.guess_entry = tk.Entry(self.frame, font=("Arial", 12))
        self.guess_entry.pack()

        self.submit_button = tk.Button(self.frame, text="Submit", command=self.check_guess, font=("Arial", 12))
        self.submit_button.pack()

    def check_guess(self):
        user_guess = self.guess_entry.get()
        if not user_guess.isdigit():
            messagebox.showinfo("Error", "Please enter a valid number.")
            return
        user_guess = int(user_guess)

        self.attempts += 1
        self.progress_var.set(self.attempts)

        if user_guess < self.secret_number:
            messagebox.showinfo("Guess Result", "Too low. Try again.")
        elif user_guess > self.secret_number:
            messagebox.showinfo("Guess Result", "Too high. Try again.")
        else:
            messagebox.showinfo("Congratulations!", f"Congratulations, {self.player_name}! You guessed the number {self.secret_number} in {self.attempts} attempts.")
            self.reset_game()
            return

        if self.attempts == self.max_attempts:
            messagebox.showinfo("Game Over", f"Game over, {self.player_name}! The secret number was {self.secret_number}.")
            self.reset_game()
            return

    def reset_game(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.guess_label.pack_forget()
        self.guess_entry.pack_forget()
        self.submit_button.pack_forget()
        self.label.config(text="Welcome to the Number Guessing Game!")
        self.name_label.pack()
        self.name_entry.pack()
        self.start_button.pack()
        self.quit_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()
