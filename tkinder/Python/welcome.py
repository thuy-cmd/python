import tkinter as tk
from tkinter import ttk
import random

reset = False
num = random.randint(1, 100)


def submit_guess(event=None):
    try:
        guess = int(entry.get())
        if guess < num:
            result.config(text="Too low. Try again!")
        elif guess > num:
            result.config(text="Too high. Try again!")
        else:
            result.config(text="🎉 Congratulations! You guessed the number!")
            reset = True
            entry.config(state="disabled")
            submit_btn.config(state="disabled")
            reset_btn.config(state="normal")
    except ValueError:
        result.config(text="Please enter a valid integer.")


def reset_game():
    global num, reset
    reset = False
    num = random.randint(1, 100)
    result.config(text="New game started. Guess a number between 1 and 100.")
    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.focus()
    submit_btn.config(state="normal")
    reset_btn.config(state="disabled")


root = tk.Tk()
root.title("Guess the Number Game")
root.geometry("420x260")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Layout
frame = ttk.Frame(root, padding=20)
frame.grid(row=0, column=0, sticky="nsew")

for c in range(3):
    frame.columnconfigure(c, weight=1)
for r in range(4):
    frame.rowconfigure(r, weight=1)

lable = ttk.Label(frame, text="Guess a number between 1 and 100")
lable.grid(row=0, column=0, columnspan=3)

entry = ttk.Entry(frame)
entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
entry.focus()
entry.bind("<Return>", submit_guess)

submit_btn = ttk.Button(frame, text="Submit Guess", command=submit_guess)
submit_btn.grid(row=1, column=2, padx=5, pady=5)

result = ttk.Label(frame, text="")
result.grid(row=3, column=0, columnspan=3, pady=(10, ))

reset_btn = ttk.Button(frame, text="Reset Game", command=reset_game,
                       state="disabled")
reset_btn.grid(row=4, column=0, columnspan=3, pady=10)
root.mainloop()
