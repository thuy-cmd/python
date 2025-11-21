import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# =============================== DATABASE ===============================

conn = sqlite3.connect('students_scores.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        masv TEXT PRIMARY KEY,
        tensv TEXT,
        lop TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        masv TEXT,
        mon TEXT,
        lan INTEGER,
        diem REAL,
        UNIQUE(masv, mon, lan),
        FOREIGN KEY(masv) REFERENCES students(masv)
    )
''')

conn.commit()

# =============================== MODEL ===============================

class Student:
    def __init__(self, masv, tensv, lop):
        self.masv = masv
        self.tensv = tensv
        self.lop = lop

class DiemThi:
    def __init__(self, mon, lan, diem):
        self.mon = mon
        self.lan = lan
        self.diem = diem

# =============================== APP ===============================

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Sinh viên & Điểm thi")
        self.students = []

        self.setup_style()

        tab = ttk.Notebook(root)
        self.tab1 = ttk.Frame(tab)
        self.tab2 = ttk.Frame(tab)
        tab.add(self.tab1, text="Quản lý Sinh viên")
        tab.add(self.tab2, text="Quản lý Điểm thi")
        tab.pack(expand=1, fill="both")

        self.build_tab1()
        self.build_tab2()

        self.load_students_from_db()

    # =============================== STYLE ===============================

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TEntry", padding=4)

    # ============================ TAB 1 (Sinh viên) ============================

    def build_tab1(self):
        tk.Label(self.tab1, text="Danh sách SV", font=("Segoe UI", 11, "bold")).grid(row=0, column=0)
        self.lstSV = tk.Listbox(self.tab1, width=20, height=15)
        self.lstSV.grid(row=1, column=0, rowspan=8, padx=10, pady=10)
        self.lstSV.bind("<<ListboxSelect>>", self.on_select_sv)

        tk.Label(self.tab1, text="Mã SV").grid(row=1, column=1, sticky='e', pady=3)
        tk.Label(self.tab1, text="Tên SV").grid(row=2, column=1, sticky='e', pady=3)
        tk.Label(self.tab1, text="Lớp").grid(row=3, column=1, sticky='e', pady=3)

        self.masv = tk.Entry(self.tab1)
        self.tensv = tk.Entry(self.tab1)
        self.lop = tk.Entry(self.tab1)
        self.masv.grid(row=1, column=2)
        self.tensv.grid(row=2, column=2)
        self.lop.grid(row=3, column=2)

        ttk.Button(self.tab1, text="Thêm", width=12, command=self.add_sv).grid(row=5, column=1, pady=5)
        ttk.Button(self.tab1, text="Sửa", width=12, command=self.update_sv).grid(row=5, column=2, pady=5)
        ttk.Button(self.tab1, text="Xóa", width=12, command=self.delete_sv).grid(row=6, column=1, pady=5)
        ttk.Button(self.tab1, text="Tìm", width=12, command=self.search_sv).grid(row=6, column=2, pady=5)

    def load_students_from_db(self):
        self.students.clear()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()

        for masv, tensv, lop in rows:
            self.students.append(Student(masv, tensv, lop))

        self.load_sv_list()

    def load_sv_list(self):
        self.lstSV.delete(0, tk.END)
        self.lstSV2.delete(0, tk.END)

        for sv in self.students:
            self.lstSV.insert(tk.END, sv.masv)
            self.lstSV2.insert(tk.END, sv.masv)

    def on_select_sv(self, event):
        if self.lstSV.curselection():
            i = self.lstSV.curselection()[0]
            sv = self.students[i]

            self.masv.delete(0, tk.END); self.masv.insert(0, sv.masv)
            self.tensv.delete(0, tk.END); self.tensv.insert(0, sv.tensv)
            self.lop.delete(0, tk.END); self.lop.insert(0, sv.lop)

    def add_sv(self):
        masv = self.masv.get()
        tensv = self.tensv.get()
        lop = self.lop.get()

        if not masv or not tensv:
            messagebox.showerror("Lỗi", "Không được bỏ trống!")
            return

        try:
            cursor.execute("INSERT INTO students VALUES (?, ?, ?)", (masv, tensv, lop))
            conn.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Mã sinh viên đã tồn tại!")
            return

        self.load_students_from_db()

    def update_sv(self):
        if not self.lstSV.curselection():
            return
        masv = self.masv.get()
        tensv = self.tensv.get()
        lop = self.lop.get()

        cursor.execute("UPDATE students SET tensv=?, lop=? WHERE masv=?", (tensv, lop, masv))
        conn.commit()

        self.load_students_from_db()

    def delete_sv(self):
        if not self.lstSV.curselection():
            return
        masv = self.masv.get()

        cursor.execute("DELETE FROM students WHERE masv=?", (masv,))
        cursor.execute("DELETE FROM scores WHERE masv=?", (masv,))
        conn.commit()

        self.load_students_from_db()

    def search_sv(self):
        masv = self.masv.get()
        cursor.execute("SELECT * FROM students WHERE masv=?", (masv,))
        sv = cursor.fetchone()

        if sv:
            messagebox.showinfo("Kết quả", f"Tên: {sv[1]}\nLớp: {sv[2]}")
        else:
            messagebox.showwarning("Không tìm thấy", "Không có sinh viên này!")

    # ============================ TAB 2 (Điểm thi) ============================

    def build_tab2(self):
        frame_left = tk.Frame(self.tab2)
        frame_left.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        tk.Label(frame_left, text="Danh sách SV").pack()
        self.lstSV2 = tk.Listbox(frame_left, width=25, height=10)
        self.lstSV2.pack()
        self.lstSV2.bind("<<ListboxSelect>>", self.on_select_sv2)

        frame_func = ttk.LabelFrame(frame_left, text="Chức năng")
        frame_func.pack(pady=5, fill=tk.X)

        tk.Label(frame_func, text="Mã SV:").grid(row=0, column=0)
        self.masv2 = tk.Entry(frame_func, width=20)
        self.masv2.grid(row=0, column=1)

        ttk.Button(frame_func, text="Nhập điểm", width=12, command=self.add_score).grid(row=0, column=2, padx=5)
        ttk.Button(frame_func, text="Sửa điểm", width=12, command=self.update_score).grid(row=1, column=0, pady=5)
        ttk.Button(frame_func, text="Xóa điểm", width=12, command=self.delete_score).grid(row=1, column=1)
        ttk.Button(frame_func, text="Xem điểm", width=12, command=self.show_score).grid(row=1, column=2)

        frame_right = tk.Frame(self.tab2)
        frame_right.pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(frame_right, text="Danh sách điểm thi").pack()
        self.lstDiem = tk.Listbox(frame_right, width=45, height=10)
        self.lstDiem.pack()

        # ⭐ GẮN SỰ KIỆN CHO DANH SÁCH ĐIỂM
        self.lstDiem.bind("<<ListboxSelect>>", self.on_select_diem)

        frame_info = ttk.LabelFrame(frame_right, text="Thông tin điểm thi")
        frame_info.pack(pady=5, fill=tk.X)

        tk.Label(frame_info, text="Môn học:").grid(row=0, column=0)
        self.mon = tk.Entry(frame_info, width=20)
        self.mon.grid(row=0, column=1)

        tk.Label(frame_info, text="Lần thi:").grid(row=1, column=0)
        self.lan = tk.Entry(frame_info, width=20)
        self.lan.grid(row=1, column=1)

        tk.Label(frame_info, text="Điểm:").grid(row=2, column=0)
        self.diem = tk.Entry(frame_info, width=20)
        self.diem.grid(row=2, column=1)

    def on_select_diem(self, event):
        if not self.lstDiem.curselection():
            return

        line = self.lstDiem.get(self.lstDiem.curselection()[0])

        if line.startswith("Chưa có điểm"):
            return

        try:
            parts = line.split("|")
            mon = parts[0].split(":")[1].strip()
            lan = parts[1].split(":")[1].strip()
            diem = parts[2].split(":")[1].strip()

            self.mon.delete(0, tk.END)
            self.mon.insert(0, mon)

            self.lan.delete(0, tk.END)
            self.lan.insert(0, lan)

            self.diem.delete(0, tk.END)
            self.diem.insert(0, diem)

        except Exception as e:
            print("Lỗi đọc dữ liệu điểm:", e)

    def on_select_sv2(self, event):
        if not self.lstSV2.curselection():
            return

        i = self.lstSV2.curselection()[0]
        masv = self.students[i].masv

        self.masv2.delete(0, tk.END)
        self.masv2.insert(0, masv)

        self.show_score()

    def add_score(self):
        masv = self.masv2.get()
        mon = self.mon.get()
        lan = self.lan.get()
        diem = self.diem.get()

        try:
            lan = int(lan)
            diem = float(diem)
        except:
            messagebox.showerror("Lỗi", "Lần thi và điểm phải là số!")
            return

        try:
            cursor.execute("INSERT INTO scores(masv, mon, lan, diem) VALUES (?, ?, ?, ?)",
                           (masv, mon, lan, diem))
            conn.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Điểm đã tồn tại!")
            return

        self.show_score()

    def show_score(self):
        self.lstDiem.delete(0, tk.END)
        masv = self.masv2.get()

        cursor.execute("SELECT mon, lan, diem FROM scores WHERE masv=?", (masv,))
        rows = cursor.fetchall()

        if not rows:
            self.lstDiem.insert(tk.END, "Chưa có điểm")
            return

        for mon, lan, diem in rows:
            self.lstDiem.insert(tk.END, f"Môn: {mon} | Lần: {lan} | Điểm: {diem}")

    def update_score(self):
        masv = self.masv2.get()
        mon = self.mon.get()
        lan = self.lan.get()

        try:
            diem = float(self.diem.get())
        except:
            messagebox.showerror("Lỗi", "Điểm phải là số!")
            return

        cursor.execute("UPDATE scores SET diem=? WHERE masv=? AND mon=? AND lan=?",
                       (diem, masv, mon, lan))
        conn.commit()

        self.show_score()

    def delete_score(self):
        masv = self.masv2.get()
        mon = self.mon.get()
        lan = self.lan.get()

        cursor.execute("DELETE FROM scores WHERE masv=? AND mon=? AND lan=?",
                       (masv, mon, lan))
        conn.commit()

        self.show_score()


root = tk.Tk()
app = App(root)
root.mainloop()
