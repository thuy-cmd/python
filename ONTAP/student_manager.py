import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_FILE = "students.db"


# ========================= DATABASE LAYER =========================
class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.create_tables()

    def create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS SinhVien(
                MaSV TEXT PRIMARY KEY,
                HoTen TEXT NOT NULL,
                Lop TEXT,
                NamSinh INTEGER
            );
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS DiemThi(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                MaSV TEXT,
                Mon TEXT NOT NULL,
                Diem REAL,
                FOREIGN KEY(MaSV) REFERENCES SinhVien(MaSV) ON DELETE CASCADE
            );
        """)
        self.conn.commit()

    # ---- SINH VIÊN ----
    def all_students(self):
        cur = self.conn.cursor()
        cur.execute("SELECT MaSV, HoTen, Lop, NamSinh FROM SinhVien ORDER BY MaSV")
        return cur.fetchall()

    def search_students(self, kw):
        kw = f"%{kw}%"
        cur = self.conn.cursor()
        cur.execute("""
            SELECT MaSV, HoTen, Lop, NamSinh FROM SinhVien
            WHERE MaSV LIKE ? OR HoTen LIKE ? OR Lop LIKE ?
            ORDER BY MaSV
        """, (kw, kw, kw))
        return cur.fetchall()

    def get_student(self, masv):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM SinhVien WHERE MaSV = ?", (masv,))
        return cur.fetchone()

    def add_student(self, masv, hoten, lop, namsinh):
        try:
            self.conn.execute(
                "INSERT INTO SinhVien VALUES(?, ?, ?, ?)",
                (masv, hoten, lop, namsinh)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_student(self, masv, hoten, lop, namsinh):
        self.conn.execute(
            "UPDATE SinhVien SET HoTen=?, Lop=?, NamSinh=? WHERE MaSV=?",
            (hoten, lop, namsinh, masv)
        )
        self.conn.commit()

    def delete_student(self, masv):
        self.conn.execute("DELETE FROM SinhVien WHERE MaSV=?", (masv,))
        self.conn.commit()

    # ---- ĐIỂM ----
    def scores_of(self, masv):
        cur = self.conn.cursor()
        cur.execute("SELECT ID, Mon, Diem FROM DiemThi WHERE MaSV=? ORDER BY ID", (masv,))
        return cur.fetchall()

    def add_score(self, masv, mon, diem):
        self.conn.execute(
            "INSERT INTO DiemThi(MaSV, Mon, Diem) VALUES (?, ?, ?)",
            (masv, mon, diem)
        )
        self.conn.commit()

    def update_score(self, sid, mon, diem):
        self.conn.execute(
            "UPDATE DiemThi SET Mon=?, Diem=? WHERE ID=?",
            (mon, diem, sid)
        )
        self.conn.commit()

    def delete_score(self, sid):
        self.conn.execute("DELETE FROM DiemThi WHERE ID=?", (sid,))
        self.conn.commit()


# ========================= GUI LAYER =========================
class App:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        root.title("Quản lý sinh viên & điểm thi")
        root.geometry("900x520")

        self.build_ui()

    # -------------------------------------------------------------
    def build_ui(self):
        nb = ttk.Notebook(self.root)
        nb.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # ========================= TAB SINH VIÊN =========================
        tab_sv = ttk.Frame(nb)
        nb.add(tab_sv, text="Sinh viên")

        # LEFT LISTBOX
        frame_left = ttk.Frame(tab_sv)
        frame_left.grid(row=0, column=0, sticky="ns", padx=5, pady=5)
        ttk.Label(frame_left, text="Danh sách sinh viên").grid(row=0, column=0, sticky="w")

        self.lb_sv = tk.Listbox(frame_left, width=25, height=22)
        self.lb_sv.grid(row=1, column=0, sticky="ns")
        self.lb_sv.bind("<<ListboxSelect>>", self.on_select_student)

        scroll = ttk.Scrollbar(frame_left, orient="vertical", command=self.lb_sv.yview)
        scroll.grid(row=1, column=1, sticky="ns")
        self.lb_sv.config(yscrollcommand=scroll.set)

        # RIGHT FORM
        frame_right = ttk.Frame(tab_sv)
        frame_right.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        labels = ["Mã SV", "Họ tên", "Lớp", "Năm sinh"]
        self.e_masv = ttk.Entry(frame_right, width=25)
        self.e_hoten = ttk.Entry(frame_right, width=40)
        self.e_lop = ttk.Entry(frame_right, width=20)
        self.e_namsinh = ttk.Entry(frame_right, width=10)

        entries = [self.e_masv, self.e_hoten, self.e_lop, self.e_namsinh]

        for i, (lbl, ent) in enumerate(zip(labels, entries)):
            ttk.Label(frame_right, text=lbl + ":").grid(row=i, column=0, sticky="w", pady=3)
            ent.grid(row=i, column=1, sticky="w", pady=3)

        # Buttons
        btns = ttk.Frame(frame_right)
        btns.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(btns, text="Thêm", command=self.add_student).grid(row=0, column=0, padx=4)
        ttk.Button(btns, text="Sửa", command=self.edit_student).grid(row=0, column=1, padx=4)
        ttk.Button(btns, text="Xóa", command=self.delete_student).grid(row=0, column=2, padx=4)

        ttk.Label(btns, text="Tìm:").grid(row=0, column=3, padx=(20,4))
        self.e_search = ttk.Entry(btns, width=20)
        self.e_search.grid(row=0, column=4, padx=4)
        ttk.Button(btns, text="Tìm", command=self.search).grid(row=0, column=5, padx=4)
        ttk.Button(btns, text="Tải lại", command=self.load_students).grid(row=0, column=6, padx=4)

        # ========================= TAB ĐIỂM THI =========================
        tab_dt = ttk.Frame(nb)
        nb.add(tab_dt, text="Điểm thi")

        # LEFT
        left = ttk.Frame(tab_dt)
        left.grid(row=0, column=0, sticky="ns", padx=5, pady=5)

        ttk.Label(left, text="Chọn sinh viên").grid(row=0, column=0, sticky="w")
        self.lb_dt = tk.Listbox(left, width=25, height=20)
        self.lb_dt.grid(row=1, column=0, sticky="ns")
        self.lb_dt.bind("<<ListboxSelect>>", self.load_scores)

        s2 = ttk.Scrollbar(left, orient="vertical", command=self.lb_dt.yview)
        s2.grid(row=1, column=1, sticky="ns")
        self.lb_dt.config(yscrollcommand=s2.set)

        # RIGHT
        right = ttk.Frame(tab_dt)
        right.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        # TREEVIEW
        self.tree = ttk.Treeview(right, columns=("id", "mon", "diem"), show="headings", height=10)
        self.tree.grid(row=0, column=0, columnspan=3, sticky="ew")

        self.tree.heading("id", text="ID")
        self.tree.heading("mon", text="Môn")
        self.tree.heading("diem", text="Điểm")

        ttk.Label(right, text="Môn:").grid(row=1, column=0, pady=5, sticky="e")
        self.e_mon = ttk.Entry(right, width=20)
        self.e_mon.grid(row=1, column=1, pady=5, sticky="w")

        ttk.Label(right, text="Điểm:").grid(row=2, column=0, pady=5, sticky="e")
        self.e_diem = ttk.Entry(right, width=10)
        self.e_diem.grid(row=2, column=1, pady=5, sticky="w")

        ttk.Button(right, text="Thêm điểm", command=self.add_score).grid(row=3, column=0, pady=6)
        ttk.Button(right, text="Sửa điểm", command=self.edit_score).grid(row=3, column=1, pady=6)
        ttk.Button(right, text="Xóa điểm", command=self.delete_score).grid(row=3, column=2, pady=6)

        self.load_students()

    # ========================= STUDENT FUNCTIONS =========================
    def load_students(self):
        self.lb_sv.delete(0, tk.END)
        self.lb_dt.delete(0, tk.END)

        for masv, _, _, _ in self.db.all_students():
            self.lb_sv.insert(tk.END, masv)
            self.lb_dt.insert(tk.END, masv)

    def on_select_student(self, *_):
        sel = self.lb_sv.curselection()
        if not sel:
            return
        masv = self.lb_sv.get(sel[0])
        sv = self.db.get_student(masv)
        if sv:
            self.e_masv.delete(0, tk.END)
            self.e_masv.insert(0, sv[0])
            self.e_hoten.delete(0, tk.END)
            self.e_hoten.insert(0, sv[1])
            self.e_lop.delete(0, tk.END)
            self.e_lop.insert(0, sv[2])
            self.e_namsinh.delete(0, tk.END)
            self.e_namsinh.insert(0, sv[3] if sv[3] else "")

    def add_student(self):
        masv = self.e_masv.get().strip()
        hoten = self.e_hoten.get().strip()
        lop = self.e_lop.get().strip()
        ns = self.e_namsinh.get().strip() or None

        if not masv or not hoten:
            messagebox.showerror("Thiếu dữ liệu", "Mã SV và Họ tên bắt buộc.")
            return

        if not self.db.add_student(masv, hoten, lop, ns):
            messagebox.showerror("Lỗi", "Mã SV đã tồn tại.")
            return

        messagebox.showinfo("OK", "Đã thêm sinh viên.")
        self.load_students()

    def edit_student(self):
        masv = self.e_masv.get().strip()
        if not masv:
            return

        self.db.update_student(
            masv,
            self.e_hoten.get(),
            self.e_lop.get(),
            self.e_namsinh.get() or None
        )
        messagebox.showinfo("OK", "Đã sửa.")
        self.load_students()

    def delete_student(self):
        sel = self.lb_sv.curselection()
        if not sel:
            return

        masv = self.lb_sv.get(sel[0])
        if messagebox.askyesno("Xác nhận", f"Xóa sinh viên {masv}?"):
            self.db.delete_student(masv)
            self.load_students()

    def search(self):
        kw = self.e_search.get().strip()
        rows = self.db.search_students(kw)

        self.lb_sv.delete(0, tk.END)
        for r in rows:
            self.lb_sv.insert(tk.END, r[0])

    # ========================= SCORE FUNCTIONS =========================
    def load_scores(self, *_):
        sel = self.lb_dt.curselection()
        if not sel:
            return

        masv = self.lb_dt.get(sel[0])
        rows = self.db.scores_of(masv)

        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert("", tk.END, values=r)

    def add_score(self):
        sel = self.lb_dt.curselection()
        if not sel:
            messagebox.showwarning("Chọn SV", "Chọn sinh viên trước.")
            return

        masv = self.lb_dt.get(sel[0])
        mon = self.e_mon.get().strip()
        diem = self.e_diem.get().strip()

        if not mon or not diem:
            return

        try:
            diem = float(diem)
        except:
            return

        self.db.add_score(masv, mon, diem)
        self.load_scores()

    def edit_score(self):
        item = self.tree.selection()
        if not item:
            return

        sid, _, _ = self.tree.item(item, "values")

        mon = self.e_mon.get().strip()
        diem = self.e_diem.get().strip()

        try:
            diem = float(diem)
        except:
            return

        self.db.update_score(sid, mon, diem)
        self.load_scores()

    def delete_score(self):
        item = self.tree.selection()
        if not item:
            return

        sid = self.tree.item(item, "values")[0]
        self.db.delete_score(sid)
        self.load_scores()


# ========================= RUN APP =========================
if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
