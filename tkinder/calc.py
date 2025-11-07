import tkinter as tk
from tkinter import ttk, messagebox

ALLOWED_CHARS = set("0123456789+-*/(). ")

def safe_eval(expr: str):
    # Chỉ cho phép các ký tự toán học đơn giản
    if not set(expr) <= ALLOWED_CHARS:
        raise ValueError("Biểu thức chứa ký tự không hợp lệ.")
    # Không cho biểu thức trống
    if expr.strip() == "":
        return ""
    # Đánh giá biểu thức trong môi trường “rỗng”
    try:
        result = eval(expr, {"__builtins__": None}, {})
    except ZeroDivisionError:
        raise ZeroDivisionError("Không thể chia cho 0.")
    except Exception:
        raise ValueError("Biểu thức không hợp lệ.")
    # Định dạng gọn: 2.0 -> 2
    if isinstance(result, float) and result.is_integer():
        result = int(result)
    return str(result)

class Calculator(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=12)
        self.expr_var = tk.StringVar(value="")
        self.build_ui()
        self.bind_keys()

    def build_ui(self):
        master = self.master
        master.title("Máy tính cầm tay - Python")
        master.resizable(False, False)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except:
            pass

        display = ttk.Entry(self, textvariable=self.expr_var, justify="right", font=("Consolas", 16))
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", ipady=8, pady=(0, 8))

        btns = [
            ("C",  1, 0), ("(",  1, 1), (")",  1, 2), ("⌫", 1, 3),
            ("7",  2, 0), ("8",  2, 1), ("9",  2, 2), ("/", 2, 3),
            ("4",  3, 0), ("5",  3, 1), ("6",  3, 2), ("*", 3, 3),
            ("1",  4, 0), ("2",  4, 1), ("3",  4, 2), ("-", 4, 3),
            ("0",  5, 0), (".",  5, 1), ("=",  5, 2), ("+", 5, 3),
        ]

        for (text, r, c) in btns:
            cmd = (lambda t=text: self.on_click(t))
            b = ttk.Button(self, text=text, command=cmd)
            b.grid(row=r, column=c, sticky="nsew", padx=4, pady=4, ipady=8)

        for i in range(6):
            self.rowconfigure(i, weight=1)
        for j in range(4):
            self.columnconfigure(j, weight=1)

        self.pack(fill="both", expand=True)

    def bind_keys(self):
        self.master.bind("<Key>", self.on_key)
        self.master.bind("<Return>", lambda e: self.on_click("="))
        self.master.bind("<KP_Enter>", lambda e: self.on_click("="))
        self.master.bind("<BackSpace>", lambda e: self.on_click("⌫"))
        self.master.bind("<Escape>", lambda e: self.on_click("C"))

    def on_key(self, event):
        ch = event.char
        if ch in ALLOWED_CHARS:
            self.expr_var.set(self.expr_var.get() + ch)

    def on_click(self, key):
        if key == "C":
            self.expr_var.set("")
        elif key == "⌫":
            self.expr_var.set(self.expr_var.get()[:-1])
        elif key == "=":
            try:
                res = safe_eval(self.expr_var.get())
                self.expr_var.set(res)
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
        else:
            self.expr_var.set(self.expr_var.get() + key)

if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
