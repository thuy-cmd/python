import tkinter as tk
from tkinter import ttk, messagebox

def add_numbers(x, y):
    return x + y

def calculate_sum(a_var, b_var):
    try:
        n1 = int(a_var.get())
        n2 = int(b_var.get())
        result = add_numbers(n1, n2)     # luôn là int
        messagebox.showinfo("Kết quả", f"Tổng là: {result}")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập các số nguyên hợp lệ.")

def main():
    root = tk.Tk()
    root.title("Chào mừng bạn đến với Tkinter")
    root.geometry("360x180")

    # Khung chính dùng grid
    frm = ttk.Frame(root, padding=12)
    frm.grid(row=0, column=0, sticky="nsew")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Cho phép ô nhập giãn theo chiều ngang
    frm.columnconfigure(1, weight=1)

    # Validate: chỉ cho nhập số nguyên (có thể âm)
    def only_int(P):
        return P == "" or P.lstrip("-").isdigit()
    vcmd = (root.register(only_int), "%P")

    # Hàng 0: Nhãn + ô nhập số thứ nhất
    ttk.Label(frm, text="Nhập số thứ nhất:").grid(row=0, column=0, sticky="w", padx=(0,8), pady=6)
    a_var = tk.StringVar()
    ttk.Entry(frm, textvariable=a_var, validate="key", validatecommand=vcmd)\
        .grid(row=0, column=1, sticky="ew", pady=6)

    # Hàng 1: Nhãn + ô nhập số thứ hai
    ttk.Label(frm, text="Nhập số thứ hai:").grid(row=1, column=0, sticky="w", padx=(0,8), pady=6)
    b_var = tk.StringVar()
    ttk.Entry(frm, textvariable=b_var, validate="key", validatecommand=vcmd)\
        .grid(row=1, column=1, sticky="ew", pady=6)

    # Hàng 2: Nút tính tổng (ngang 2 cột)
    ttk.Button(frm, text="Tính tổng", command=lambda: calculate_sum(a_var, b_var))\
        .grid(row=2, column=0, columnspan=2, pady=12, sticky="e")

    # Enter để tính nhanh
    root.bind("<Return>", lambda _e: calculate_sum(a_var, b_var))

    root.mainloop()

if __name__ == "__main__":
    main()
