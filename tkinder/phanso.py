import tkinter as tk
from tkinter import ttk
from fractions import Fraction

class FractionBox(ttk.Frame):
    def __init__(self, master, num="", den="", **kw):
        super().__init__(master, **kw)
        self.num_var = tk.StringVar(value=str(num))
        self.den_var = tk.StringVar(value=str(den))

        def only_int(P):
            return P in ("", "-") or P.lstrip("-").isdigit()
        vcmd = (self.register(only_int), "%P")

        e_num = ttk.Entry(self, width=8, justify="center",
                          textvariable=self.num_var, validate="key", validatecommand=vcmd)
        sep   = ttk.Separator(self, orient="horizontal")
        e_den = ttk.Entry(self, width=8, justify="center",
                          textvariable=self.den_var, validate="key", validatecommand=vcmd)
        e_num.grid(row=0, column=0, sticky="ew")
        sep.grid(row=1, column=0, sticky="ew", pady=2)
        e_den.grid(row=2, column=0, sticky="ew")
        self.columnconfigure(0, weight=1)

    def get_fraction(self) -> Fraction | None:
        n_txt, d_txt = self.num_var.get(), self.den_var.get()
        n = 0 if n_txt in ("", "-") else int(n_txt)
        d = 1 if d_txt in ("", "-") or d_txt == "" else int(d_txt)
        if d == 0:
            return None
        return Fraction(n, d)

    def trace(self, cb):
        self.num_var.trace_add("write", lambda *_: cb())
        self.den_var.trace_add("write", lambda *_: cb())

# ===== Nhãn hiển thị phân số =====
class FractionLabel(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.l_num = ttk.Label(self, text="0", anchor="center", width=8)
        sep       = ttk.Separator(self, orient="horizontal")
        self.l_den = ttk.Label(self, text="1", anchor="center", width=8)
        self.l_num.grid(row=0, column=0, sticky="ew")
        sep.grid(row=1, column=0, sticky="ew", pady=2)
        self.l_den.grid(row=2, column=0, sticky="ew")
        self.columnconfigure(0, weight=1)

    def set_fraction(self, f: Fraction | None):
        if f is None:
            self.l_num.config(text="—"); self.l_den.config(text="0")
        else:
            self.l_num.config(text=str(f.numerator))
            self.l_den.config(text=str(f.denominator))

def main():
    root = tk.Tk()
    root.title("Phân số - Python")
    root.geometry("400x200")

    wrap = ttk.Frame(root, padding=16)
    wrap.pack(fill="both", expand=True)

    # Cột: 0 (Số thứ nhất) | 1 (dấu) | 2 (Số thứ hai) | 3 (=) | 4 (Kết quả)
    for c in range(5):
        wrap.columnconfigure(c, weight=1)

    # Tiêu đề cột
    ttk.Label(wrap, text="Số thứ nhất", anchor="center").grid(row=0, column=0, pady=(0,8))
    ttk.Label(wrap, text="Số thứ hai",  anchor="center").grid(row=0, column=2, pady=(0,8))
    ttk.Label(wrap, text="Kết quả",     anchor="center").grid(row=0, column=4, pady=(0,8))

    # ===== DÒNG 1: CỘNG =====
    a1 = FractionBox(wrap, "1", "2")
    b1 = FractionBox(wrap, "2", "3")
    r1 = FractionLabel(wrap)
    a1.grid(row=1, column=0, sticky="n", padx=10, pady=6)
    ttk.Label(wrap, text="+", anchor="center").grid(row=1, column=1)
    b1.grid(row=1, column=2, sticky="n", padx=10, pady=6)
    ttk.Label(wrap, text="=", anchor="center").grid(row=1, column=3)
    r1.grid(row=1, column=4, sticky="n", padx=10, pady=6)

    # ===== DÒNG 2: NHÂN =====
    a2 = FractionBox(wrap, "2", "3")
    b2 = FractionBox(wrap, "1", "6")
    r2 = FractionLabel(wrap)
    a2.grid(row=2, column=0, sticky="n", padx=10, pady=6)
    ttk.Label(wrap, text="×", anchor="center").grid(row=2, column=1)
    b2.grid(row=2, column=2, sticky="n", padx=10, pady=6)
    ttk.Label(wrap, text="=", anchor="center").grid(row=2, column=3)
    r2.grid(row=2, column=4, sticky="n", padx=10, pady=6)

    # ===== TÍNH TOÁN & CẬP NHẬT =====
    def calc_row(op, left: Fraction | None, right: Fraction | None) -> Fraction | None:
        if left is None or right is None:
            return None
        return left + right if op == "+" else left * right

    def recalc(*_):
        r1.set_fraction(calc_row("+", a1.get_fraction(), b1.get_fraction()))
        r2.set_fraction(calc_row("×", a2.get_fraction(), b2.get_fraction()))

    # Gắn theo dõi thay đổi
    for fb in (a1, b1, a2, b2):
        fb.trace(recalc)

    root.bind("<Return>", recalc)
    recalc()

    root.mainloop()

if __name__ == "__main__":
    main()
