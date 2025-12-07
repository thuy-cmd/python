import sqlite3
import tkinter as tk
from tkinter import messagebox

DB_FILE = "sinhvien.db"

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        major TEXT
    )
    """)
    conn.commit()
    conn.close()

def db_insert(name, age, major):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, age, major) VALUES (?, ?, ?)", (name, age, major))
    conn.commit()
    conn.close()

def db_update(sid, name, age, major):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("UPDATE students SET name=?, age=?, major=? WHERE id=?", (name, age, major, sid))
    conn.commit()
    conn.close()

def db_delete(sid):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (sid,))
    conn.commit()
    conn.close()

def db_fetch_all():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM students ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return rows

def db_search(keyword):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE name LIKE ? ORDER BY id", ('%'+keyword+'%',))
    rows = cur.fetchall()
    conn.close()
    return rows

# ---------- GUI ----------
class App:
    def __init__(self, root):
        self.root = root
        root.title("Quản lý Sinh viên - Tkinter + SQLite")
        root.geometry("640x420")
        root.resizable(False, False)

        # Variables
        self.var_id = None  # lưu id của record đang chọn
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.major_var = tk.StringVar()
        self.search_var = tk.StringVar()

        # --- Top frame: form ---
        frm_form = tk.Frame(root, padx=10, pady=10, bd=1, relief="groove")
        frm_form.place(x=10, y=10, width=380, height=160)

        tk.Label(frm_form, text="Tên:").grid(row=0, column=0, sticky="e", pady=4)
        self.e_name = tk.Entry(frm_form, textvariable=self.name_var, width=30)
        self.e_name.grid(row=0, column=1, padx=6, pady=4, sticky="w")

        tk.Label(frm_form, text="Tuổi:").grid(row=1, column=0, sticky="e", pady=4)
        # validate tuổi chỉ cho số
        vcmd = (root.register(self.validate_age), "%P")
        self.e_age = tk.Entry(frm_form, textvariable=self.age_var, width=10, validate="key", validatecommand=vcmd)
        self.e_age.grid(row=1, column=1, padx=6, pady=4, sticky="w")

        tk.Label(frm_form, text="Ngành:").grid(row=2, column=0, sticky="e", pady=4)
        self.e_major = tk.Entry(frm_form, textvariable=self.major_var, width=30)
        self.e_major.grid(row=2, column=1, padx=6, pady=4, sticky="w")

        # Buttons in form
        btn_frame = tk.Frame(frm_form)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=8)
        tk.Button(btn_frame, text="Thêm", width=10, command=self.add_student).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Cập nhật", width=10, command=self.update_student).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Xóa", width=10, command=self.delete_student).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Clear", width=8, command=self.clear_form).pack(side="left", padx=6)

        # --- Right/top: search ---
        frm_search = tk.Frame(root, padx=10, pady=10, bd=1, relief="groove")
        frm_search.place(x=400, y=10, width=230, height=160)

        tk.Label(frm_search, text="Tìm theo tên:").pack(anchor="w")
        search_box = tk.Entry(frm_search, textvariable=self.search_var, width=25)
        search_box.pack(pady=4)
        tk.Button(frm_search, text="Tìm", width=10, command=self.search).pack(pady=4)
        tk.Button(frm_search, text="Hiện tất cả", width=10, command=self.load_list).pack()

        # --- Listbox area ---
        frm_list = tk.Frame(root, padx=10, pady=10)
        frm_list.place(x=10, y=180, width=620, height=220)

        self.lb = tk.Listbox(frm_list, height=10, selectmode="browse")
        self.lb.pack(side="left", fill="both", expand=True)
        self.lb.bind("<<ListboxSelect>>", self.on_select)

        scrollbar = tk.Scrollbar(frm_list, orient="vertical", command=self.lb.yview)
        scrollbar.pack(side="right", fill="y")
        self.lb.config(yscrollcommand=scrollbar.set)

        # load data
        self.load_list()

    # validate tuổi: chỉ chữ số hoặc rỗng
    def validate_age(self, P):
        if P == "" or P.isdigit():
            return True
        return False

    def add_student(self):
        name = self.name_var.get().strip()
        age = self.age_var.get().strip()
        major = self.major_var.get().strip()
        if not name:
            messagebox.showwarning("Lỗi", "Tên không được bỏ trống")
            return
        age_int = int(age) if age else None
        db_insert(name, age_int, major)
        messagebox.showinfo("Thành công", "Đã thêm sinh viên")
        self.clear_form()
        self.load_list()

    def update_student(self):
        if not self.var_id:
            messagebox.showwarning("Lỗi", "Chưa chọn sinh viên để cập nhật")
            return
        name = self.name_var.get().strip()
        age = self.age_var.get().strip()
        major = self.major_var.get().strip()
        if not name:
            messagebox.showwarning("Lỗi", "Tên không được bỏ trống")
            return
        age_int = int(age) if age else None
        db_update(self.var_id, name, age_int, major)
        messagebox.showinfo("Thành công", "Đã cập nhật sinh viên")
        self.clear_form()
        self.load_list()

    def delete_student(self):
        if not self.var_id:
            messagebox.showwarning("Lỗi", "Chưa chọn sinh viên để xóa")
            return
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa bản ghi này?"):
            return
        db_delete(self.var_id)
        messagebox.showinfo("Đã xóa", "Xóa thành công")
        self.clear_form()
        self.load_list()

    def clear_form(self):
        self.var_id = None
        self.name_var.set("")
        self.age_var.set("")
        self.major_var.set("")
        self.lb.selection_clear(0, tk.END)

    def load_list(self):
        self.lb.delete(0, tk.END)
        rows = db_fetch_all()
        for r in rows:
            # r = (id, name, age, major)
            display = f"{r[0]:>3} | {r[1]:<20} | {'' if r[2] is None else r[2]:>3} tuổi | {r[3]}"
            self.lb.insert(tk.END, display)

    def search(self):
        kw = self.search_var.get().strip()
        self.lb.delete(0, tk.END)
        if not kw:
            self.load_list()
            return
        rows = db_search(kw)
        for r in rows:
            display = f"{r[0]:>3} | {r[1]:<20} | {'' if r[2] is None else r[2]:>3} tuổi | {r[3]}"
            self.lb.insert(tk.END, display)

    def on_select(self, event):
        sel = self.lb.curselection()
        if not sel:
            return
        idx = sel[0]
        txt = self.lb.get(idx)
        # định dạng hiển thị là: " id | name | age tuổi | major"
        # ta parse id bằng split
        try:
            sid_str = txt.split("|", 1)[0].strip()
            sid = int(sid_str)
        except Exception:
            messagebox.showerror("Lỗi", "Không lấy được id từ dòng chọn")
            return
        # load record từ DB để đảm bảo lấy đúng dữ liệu
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE id=?", (sid,))
        row = cur.fetchone()
        conn.close()
        if not row:
            messagebox.showerror("Lỗi", "Bản ghi không tồn tại")
            return
        self.var_id = row[0]
        self.name_var.set(row[1] or "")
        self.age_var.set("" if row[2] is None else str(row[2]))
        self.major_var.set(row[3] or "")

# ---------- main ----------
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
