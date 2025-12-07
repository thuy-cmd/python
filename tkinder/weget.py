import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Ví dụ nhanh")

# Frame trên
top = tk.Frame(root, padx=8, pady=8)
top.pack(fill="x")
tk.Label(top, text="Label ví dụ", font=("Arial",14)).pack(side="left")

# Entry + Button
entry_var = tk.StringVar()
e = tk.Entry(root, textvariable=entry_var, width=30)
e.pack(pady=6)

def add_item():
    val = entry_var.get().strip()
    if not val:
        messagebox.showwarning("Lỗi", "Chưa nhập gì")
        return
    lb.insert("end", val)
    entry_var.set("")

tk.Button(root, text="Thêm vào Listbox", command=add_item).pack()

# Listbox + Scrollbar
frame_lb = tk.Frame(root)
frame_lb.pack(pady=6)
scroll = tk.Scrollbar(frame_lb, orient="vertical")
lb = tk.Listbox(frame_lb, height=6, yscrollcommand=scroll.set, selectmode="single")
scroll.config(command=lb.yview)
lb.pack(side="left")
scroll.pack(side="left", fill="y")

# Checkbutton + Radiobutton
cb_var = tk.IntVar(value=0)
tk.Checkbutton(root, text="Bật chức năng", variable=cb_var).pack()

rb_var = tk.StringVar(value="opt1")
tk.Radiobutton(root, text="Option 1", variable=rb_var, value="opt1").pack(anchor="w")
tk.Radiobutton(root, text="Option 2", variable=rb_var, value="opt2").pack(anchor="w")

# Nút thoát
tk.Button(root, text="Thoát", command=root.destroy).pack(pady=6)

root.mainloop()
