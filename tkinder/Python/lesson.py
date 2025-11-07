import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Simple Tkinter Window")
root.geometry("400x200")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

v = tk.StringVar(value="")


def choose(event=None):
    label.config(text=f"You just choose: {v.get()}")


male_btn = ttk.Radiobutton(
    root, text="Male", variable=v, value="Male", command=choose)
male_btn.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
female_btn = ttk.Radiobutton(
    root, text="Female", variable=v, value="Female", command=choose)
female_btn.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

label = ttk.Label(root, text="Pick one")
label.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

root.mainloop()
