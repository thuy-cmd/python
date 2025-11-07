import tkinter as tk
from tkinter import ttk
from fractions import Fraction

def main():
    root = tk.Tk()
    root.title("Phân số")
    root.geometry("400x200")

    wrap = ttk.Frame(root, padding=16)
    wrap.pack(fill="both", expand=True)

    for c in range(5):
        wrap.columnconfigure(c, weight=1)

    tk.Label(wrap, text="Số thứ nhất", anchor="center").grid(row=0, column=0, pady=(0,8))
    tk.Label(wrap, text="Số thứ hai",  anchor="center").grid(row=0, column=2, pady=(0,8))
    tk.Label(wrap, text="Kết quả",     anchor="center").grid(row=0, column=4, pady=(0,8))
    # ===== DÒNG 1: CỘNG =====
    a1 = ttk.Entry(wrap)
    a1.grid(row=1, column=0, sticky="n", padx=10, pady=6)
    tk.Label(wrap, text="+", anchor="center").grid(row=1, column=1)
    b1 = ttk.Entry(wrap)
    b1.grid(row=1, column=2, sticky="n", padx=10, pady=6)
    tk.Label(wrap, text="=", anchor="center").grid(row=1, column=3)
    r1 = ttk.Label(wrap, text="")
    r1.grid(row=1, column=4, sticky="n", padx=10, pady=6)
    root.mainloop()

if __name__ == "__main__":
    main()
