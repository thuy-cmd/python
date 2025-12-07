import tkinter as tk
from tkinter import ttk, messagebox, Listbox

def change_state():
    button.config(state="normal")

def click():
    cur_name = name.get()
    messagebox.showinfo("Clik me", f"Hello {cur_name}! You just click me")

root = tk.Tk()
root.title("Cách dùng các widget kèm ví dụ")
root.geometry("400x300")

name = tk.StringVar(value="")

frame = ttk.Frame(root, padding=12)
frame.grid(row=0, column=0,sticky="nsew")

label = ttk.Label(frame,
                text="Đối tượng Label",
                foreground="#ccc",
                background="darkgreen",
                padding=(10,6),
                relief="ridge"
        )
label.grid(row=0, column=0)

button = ttk.Button(frame,
                text="Click me",
                command=click,
                state="disabled"
        )
button.grid(row=0, column=1)

entry = tk.Entry(frame,
                textvariable=name,
                width=30,
                justify="left",
                state="normal"
        )
entry.grid(row=1, column=0)

button_change = tk.Button(frame,
                text="Change state",
                command=change_state
            )
button_change.grid(row=2, column=0)

list_n = Listbox(frame, height=5, border=1)
list_n.grid(row=3, column=0)

for i in range(10):
    list_n.insert("end", f"Sản phẩm thứ {i}")

scroll = tk.Scrollbar(frame, orient="vertical", command=list_n.yview)
scroll.grid(row=3, column=1, sticky="ns")
list_n.config(yscrollcommand=scroll.set)

root.mainloop()
