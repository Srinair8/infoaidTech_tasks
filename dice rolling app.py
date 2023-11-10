import tkinter as tk
import random

class DiceRollingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dice Rolling App")
        self.root.geometry("300x250")
        self.root.configure(bg="lightgray")  # Set background color

        self.label = tk.Label(root, text="Welcome to the Dice Rolling App!", font=("Arial", 14), bg="lightgray")
        self.label.pack(pady=10)

        self.num_dice_label = tk.Label(root, text="Select the number of dice to roll:", font=("Arial", 12), bg="lightgray")
        self.num_dice_label.pack()

        self.num_dice_var = tk.StringVar()
        self.num_dice_var.set("1")  # Default value
        self.num_dice_options = ["1", "2", "3", "4", "5", "6"]
        self.num_dice_menu = tk.OptionMenu(root, self.num_dice_var, *self.num_dice_options)
        self.num_dice_menu.configure(bg="lightblue")  # Set background color
        self.num_dice_menu.pack()

        self.roll_button = tk.Button(root, text="Roll Dice", command=self.roll_dice, font=("Arial", 12), bg="lightgreen")  # Set background color
        self.roll_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 16), bg="lightgray")
        self.result_label.pack()

        self.roll_again_button = tk.Button(root, text="Roll Again", command=self.roll_dice, font=("Arial", 12), bg="lightgreen")  # Set background color
        self.roll_again_button.pack()
        self.roll_again_button.pack_forget()  # Initially hidden

        self.quit_button = tk.Button(root, text="Quit", command=root.destroy, font=("Arial", 12), bg="red")  # Set background color
        self.quit_button.pack()

    def roll_dice(self):
        num_dice = int(self.num_dice_var.get())
        rolls = [random.randint(1, 6) for _ in range(num_dice)]
        result = "Dice Roll Result: " + " ".join(map(str, rolls))
        self.result_label.config(text=result)

        self.roll_button.pack_forget()
        self.roll_again_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = DiceRollingApp(root)
    root.mainloop()
