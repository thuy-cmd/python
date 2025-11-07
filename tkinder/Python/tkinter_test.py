import tkinter as tk
from tkinter import ttk


def add_to_list(entry_widget, list_widget, event=None):
    text = entry_widget.get().strip()
    if text:
        list_widget.insert(tk.END, text)
        entry_widget.delete(0, tk.END)


root = tk.Tk()
root.title("Simple Tkinter Window")
root.geometry("640x260")

# chia 2 cột cho 2 khung
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

# ===== Khung trái (ttk) =====
frame1 = ttk.Frame(root, padding=10)
frame1.grid(row=0, column=0, sticky="nsew")
frame1.columnconfigure(0, weight=1)
frame1.rowconfigure(1, weight=1)

entry1 = ttk.Entry(frame1, width=30)
entry1.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

list1 = tk.Listbox(frame1, width=40, height=8)
list1.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

btn1 = ttk.Button(frame1, text="Submit",
                  command=lambda: add_to_list(entry1, list1))
btn1.grid(row=0, column=1, padx=5, pady=5)

entry1.focus()
entry1.bind("<Return>", lambda e: add_to_list(entry1, list1))

# ===== Khung phải (tk) =====
frame2 = tk.Frame(root, padx=10, pady=10)
frame2.grid(row=0, column=1, sticky="nsew")
frame2.columnconfigure(0, weight=1)
frame2.rowconfigure(1, weight=1)

entry2 = tk.Entry(frame2, width=30)
entry2.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

list2 = tk.Listbox(frame2, width=40, height=8)
list2.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

btn2 = tk.Button(frame2, text="Submit",
                 command=lambda: add_to_list(entry2, list2))
btn2.grid(row=0, column=1, padx=5, pady=5)

entry2.bind("<Return>", lambda e: add_to_list(entry2, list2))

root.mainloop()
