import sqlite3
import tkinter as tk
from tkinter import ttk, Listbox, messagebox

DB_FILE = "products.db"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý sản phẩm")
        self.root.geometry("720x440")
        self.root.minsize(600, 380)

        # Variables
        self.masp = tk.StringVar()
        self.tensp = tk.StringVar()
        self.hangsx = tk.StringVar()
        self.namsx = tk.StringVar()
        self.search_var = tk.StringVar()

        # DB
        self.conn = None
        self._connect_db()

        # Build UI
        self._create_main_frame()
        self._create_controls()
        self._create_search()
        self._create_listbox()
        self._bind_events()

        # Load products
        self.load_products()

    # ----------------- Database -----------------
    def _connect_db(self):
        self.conn = sqlite3.connect(DB_FILE)
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT,
                name TEXT NOT NULL,
                brand TEXT,
                year INTEGER
            )
            """
        )
        self.conn.commit()

    def _execute(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        return cur

    # ----------------- UI building -----------------
    def _create_main_frame(self):
        self.frame = ttk.Frame(self.root, padding=12, relief="groove")
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Make frame grid responsive: row 0 inputs, row1 listbox grows
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)  # form + list on left
        self.frame.columnconfigure(1, weight=0)  # search panel (kept small)

    def _create_controls(self):
        self.frame_control = ttk.Frame(self.frame)
        self.frame_control.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        # configure columns inside control frame
        self.frame_control.columnconfigure(0, weight=0)  # labels
        self.frame_control.columnconfigure(1, weight=1)  # entries
        self.frame_control.columnconfigure(2, weight=0)  # optional extra

        # Labels + Entries (use self.* so available for methods)
        ttk.Label(self.frame_control, text="Mã sản phẩm:").grid(row=0, column=0, sticky="w")
        self.entry_id = ttk.Entry(self.frame_control, textvariable=self.masp)
        self.entry_id.grid(row=0, column=1, sticky="ew", pady=6, padx=6, columnspan=2)

        ttk.Label(self.frame_control, text="Tên sản phẩm:").grid(row=1, column=0, sticky="w")
        self.entry_name = ttk.Entry(self.frame_control, textvariable=self.tensp)
        self.entry_name.grid(row=1, column=1, sticky="ew", pady=6, padx=6, columnspan=2)

        ttk.Label(self.frame_control, text="Hãng sản xuất:").grid(row=2, column=0, sticky="w")
        self.entry_brand = ttk.Entry(self.frame_control, textvariable=self.hangsx)
        self.entry_brand.grid(row=2, column=1, sticky="ew", pady=6, padx=6, columnspan=2)

        ttk.Label(self.frame_control, text="Năm sản xuất:").grid(row=3, column=0, sticky="w")
        self.entry_year = ttk.Entry(self.frame_control, textvariable=self.namsx)
        self.entry_year.grid(row=3, column=1, sticky="ew", pady=6, padx=6, columnspan=2)

        # Buttons row
        self.btn_add = ttk.Button(self.frame_control, text="Thêm", command=self.add_product)
        self.btn_add.grid(row=4, column=0, sticky="ew", padx=6, pady=6)

        self.btn_edit = ttk.Button(self.frame_control, text="Sửa", command=self.edit_product)
        self.btn_edit.grid(row=4, column=1, sticky="ew", padx=6, pady=6)

        self.btn_delete = ttk.Button(self.frame_control, text="Xóa", command=self.delete_product)
        self.btn_delete.grid(row=4, column=2, sticky="ew", padx=6, pady=6)

    def _create_search(self):
        self.frame_search = ttk.Frame(self.frame)
        self.frame_search.grid(row=0, column=1, sticky="nsew")
        self.frame_search.columnconfigure(0, weight=1)

        ttk.Label(self.frame_search, text="Tìm kiếm theo tên sản phẩm").grid(row=0, column=0, sticky="w")
        self.entry_search = ttk.Entry(self.frame_search, textvariable=self.search_var)
        self.entry_search.grid(row=1, column=0, sticky="ew", padx=6, pady=6)

        self.btn_search = ttk.Button(self.frame_search, text="Tìm kiếm", command=self.search_products)
        self.btn_search.grid(row=2, column=0, sticky="ew", padx=6, pady=6)

        self.btn_clear_search = ttk.Button(self.frame_search, text="Xóa tìm kiếm", command=self.clear_search)
        self.btn_clear_search.grid(row=3, column=0, sticky="ew", padx=6, pady=(0,6))

    def _create_listbox(self):
        # Container to allow padding and better control
        lb_frame = ttk.Frame(self.frame)
        lb_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=6)
        lb_frame.rowconfigure(0, weight=1)
        lb_frame.columnconfigure(0, weight=1)

        self.list_products = Listbox(lb_frame, height=8)
        self.list_products.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(lb_frame, orient="vertical", command=self.list_products.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.list_products.configure(yscrollcommand=scrollbar.set)

    def _bind_events(self):
        self.list_products.bind("<<ListboxSelect>>", self.on_select)
        self.root.bind("<Return>", lambda event: self.add_product())  # optional: Enter adds

    # ----------------- CRUD operations -----------------
    def load_products(self):
        self.list_products.delete(0, tk.END)
        cur = self._execute("SELECT id, code, name, brand, year FROM products ORDER BY id")
        for row in cur.fetchall():
            idx, code, name, brand, year = row
            display = f"{idx}: {code or ''} - {name} - {brand or ''} - {year or ''}"
            self.list_products.insert(tk.END, display)

    def add_product(self):
        name = self.tensp.get().strip()
        if not name:
            messagebox.showwarning("Thiếu dữ liệu", "Tên sản phẩm không được để trống.")
            return
        code = self.masp.get().strip() or None
        brand = self.hangsx.get().strip() or None
        year = self.namsx.get().strip() or None
        try:
            year_val = int(year) if year else None
        except ValueError:
            messagebox.showwarning("Dữ liệu sai", "Năm sản xuất phải là số.")
            return

        self._execute(
            "INSERT INTO products (code, name, brand, year) VALUES (?, ?, ?, ?)",
            (code, name, brand, year_val)
        )
        self.clear_entries()
        self.load_products()

    def edit_product(self):
        sel = self._get_selected_id()
        if sel is None:
            messagebox.showinfo("Chọn sản phẩm", "Hãy chọn sản phẩm để sửa.")
            return
        name = self.tensp.get().strip()
        if not name:
            messagebox.showwarning("Thiếu dữ liệu", "Tên sản phẩm không được để trống.")
            return
        code = self.masp.get().strip() or None
        brand = self.hangsx.get().strip() or None
        year = self.namsx.get().strip() or None
        try:
            year_val = int(year) if year else None
        except ValueError:
            messagebox.showwarning("Dữ liệu sai", "Năm sản xuất phải là số.")
            return

        self._execute(
            "UPDATE products SET code=?, name=?, brand=?, year=? WHERE id=?",
            (code, name, brand, year_val, sel)
        )
        self.clear_entries()
        self.load_products()

    def delete_product(self):
        sel = self._get_selected_id()
        if sel is None:
            messagebox.showinfo("Chọn sản phẩm", "Hãy chọn sản phẩm để xóa.")
            return
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa sản phẩm này?"):
            return
        self._execute("DELETE FROM products WHERE id=?", (sel,))
        self.clear_entries()
        self.load_products()

    def search_products(self):
        kw = self.search_var.get().strip()
        self.list_products.delete(0, tk.END)
        if not kw:
            self.load_products()
            return
        cur = self._execute("SELECT id, code, name, brand, year FROM products WHERE name LIKE ? ORDER BY id",
                            (f"%{kw}%",))
        for row in cur.fetchall():
            idx, code, name, brand, year = row
            display = f"{idx}: {code or ''} - {name} - {brand or ''} - {year or ''}"
            self.list_products.insert(tk.END, display)

    def clear_search(self):
        self.search_var.set("")
        self.load_products()

    # ----------------- Helpers -----------------
    def on_select(self, event):
        idx = self.list_products.curselection()
        if not idx:
            return
        text = self.list_products.get(idx)
        # Stored format: "id: code - name - brand - year"
        try:
            id_part = text.split(":", 1)[0].strip()
            prod_id = int(id_part)
        except Exception:
            return
        cur = self._execute("SELECT code, name, brand, year FROM products WHERE id=?", (prod_id,))
        row = cur.fetchone()
        if row:
            code, name, brand, year = row
            self.masp.set(code or "")
            self.tensp.set(name or "")
            self.hangsx.set(brand or "")
            self.namsx.set(str(year) if year is not None else "")

    def _get_selected_id(self):
        sel = self.list_products.curselection()
        if not sel:
            return None
        text = self.list_products.get(sel)
        try:
            id_part = text.split(":", 1)[0].strip()
            return int(id_part)
        except Exception:
            return None

    def clear_entries(self):
        self.masp.set("")
        self.tensp.set("")
        self.hangsx.set("")
        self.namsx.set("")
        self.list_products.selection_clear(0, tk.END)

    # ----------------- Cleanup -----------------
    def close(self):
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    try:
        root.mainloop()
    finally:
        app.close()
