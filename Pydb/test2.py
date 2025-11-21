import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect('students_scores.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        masv TEXT UNIQUE,
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

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Sinh viên & Điểm thi")
        self.students = []
        self.ds_diem = {}

        tab = ttk.Notebook(root)
        self.tab1 = ttk.Frame(tab)
        self.tab2 = ttk.Frame(tab)
        tab.add(self.tab1, text="Quản lý Sinh viên")
        tab.add(self.tab2, text="Quản lý Điểm thi")
        tab.pack(expand=1, fill="both")

        self.build_tab1()
        self.build_tab2()

    # ================= TAB 1 =================
    def build_tab1(self):
        tk.Label(self.tab1, text="Danh sách SV").grid(row=0, column=0)
        self.lstSV = tk.Listbox(self.tab1, width=20, height=15)
        self.lstSV.grid(row=1, column=0, rowspan=8, padx=10)
        self.lstSV.bind("<<ListboxSelect>>", self.on_select_sv)

        tk.Label(self.tab1, text="Mã SV").grid(row=1, column=1, sticky='e')
        tk.Label(self.tab1, text="Tên SV").grid(row=2, column=1, sticky='e')
        tk.Label(self.tab1, text="Lớp").grid(row=3, column=1, sticky='e')

        self.masv = tk.Entry(self.tab1)
        self.tensv = tk.Entry(self.tab1)
        self.lop = tk.Entry(self.tab1)
        self.masv.grid(row=1, column=2)
        self.tensv.grid(row=2, column=2)
        self.lop.grid(row=3, column=2)

        tk.Button(self.tab1, text="Thêm", width=10, command=self.add_sv).grid(row=4, column=1)
        tk.Button(self.tab1, text="Sửa", width=10, command=self.update_sv).grid(row=4, column=2)
        tk.Button(self.tab1, text="Xóa", width=10, command=self.delete_sv).grid(row=5, column=1)
        tk.Button(self.tab1, text="Tìm", width=10, command=self.search_sv).grid(row=5, column=2)

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
        if any(sv.masv == masv for sv in self.students):
            messagebox.showerror("Lỗi", "Mã sinh viên đã tồn tại!")
            return
        sv = Student(masv, self.tensv.get(), self.lop.get())
        self.students.append(sv)
        self.load_sv_list()

    def update_sv(self):
        if self.lstSV.curselection():
            i = self.lstSV.curselection()[0]
            sv = self.students[i]
            sv.masv = self.masv.get()
            sv.tensv = self.tensv.get()
            sv.lop = self.lop.get()
            self.load_sv_list()

    def delete_sv(self):
        if self.lstSV.curselection():
            i = self.lstSV.curselection()[0]
            self.students.pop(i)
            self.load_sv_list()

    def search_sv(self):
        masv = self.masv.get()
        for sv in self.students:
            if sv.masv == masv:
                messagebox.showinfo("Kết quả", f"Tên: {sv.tensv}\nLớp: {sv.lop}")
                return
        messagebox.showwarning("Không tìm thấy", "Không có sinh viên này!")

    # ================= TAB 2 =================
    def build_tab2(self):
        # Khung trái: danh sách SV + chức năng
        frame_left = tk.Frame(self.tab2)
        frame_left.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        # Danh sách SV
        tk.Label(frame_left, text="Danh sách SV").pack()
        self.lstSV2 = tk.Listbox(frame_left, width=25, height=10)
        self.lstSV2.pack()
        self.lstSV2.bind("<<ListboxSelect>>", self.on_select_sv2)

        # Chức năng bên dưới danh sách SV
        frame_func = tk.LabelFrame(frame_left, text="Chức năng")
        frame_func.pack(pady=5, fill=tk.X)
        tk.Label(frame_func, text="Mã SV:").grid(row=0, column=0)
        self.masv2 = tk.Entry(frame_func, width=20)
        self.masv2.grid(row=0, column=1)
        tk.Button(frame_func, text="Nhập điểm", width=12, command=self.add_score).grid(row=0, column=2, padx=5)
        tk.Button(frame_func, text="Sửa điểm", width=12, command=self.update_score).grid(row=1, column=0, pady=5)
        tk.Button(frame_func, text="Xóa điểm", width=12, command=self.delete_score).grid(row=1, column=1)
        tk.Button(frame_func, text="Xem điểm", width=12, command=self.show_score).grid(row=1, column=2)

        # Khung phải: danh sách điểm + thông tin chi tiết
        frame_right = tk.Frame(self.tab2)
        frame_right.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        tk.Label(frame_right, text="Danh sách điểm thi").pack()
        self.lstDiem = tk.Listbox(frame_right, width=40, height=10)
        self.lstDiem.pack()

        # Thông tin chi tiết điểm thi
        frame_info = tk.LabelFrame(frame_right, text="Thông tin điểm thi")
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

    # ================= Điểm thi =================
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
        if masv not in [sv.masv for sv in self.students]:
            messagebox.showerror("Lỗi", "Mã SV không tồn tại!")
            return
        try:
            diem = float(diem)
        except:
            messagebox.showerror("Lỗi", "Điểm phải là số!")
            return
        if masv not in self.ds_diem:
            self.ds_diem[masv] = []
        for d in self.ds_diem[masv]:
            if d.mon == mon and d.lan == lan:
                messagebox.showerror("Lỗi", "Điểm đã tồn tại!")
                return
        self.ds_diem[masv].append(DiemThi(mon, lan, diem))
        self.show_score()
        messagebox.showinfo("OK", "Đã lưu điểm!")

    def show_score(self):
        self.lstDiem.delete(0, tk.END)
        masv = self.masv2.get()
        if masv in self.ds_diem:
            for d in self.ds_diem[masv]:
                self.lstDiem.insert(tk.END, f"Môn: {d.mon} | Lần: {d.lan} | Điểm: {d.diem}")
        else:
            self.lstDiem.insert(tk.END, "Chưa có điểm")

    def update_score(self):
        masv = self.masv2.get()
        mon = self.mon.get()
        lan = self.lan.get()
        diem = self.diem.get()
        if masv not in self.ds_diem:
            messagebox.showerror("Lỗi", "Chưa có điểm để sửa!")
            return
        for d in self.ds_diem[masv]:
            if d.mon == mon and d.lan == lan:
                try:
                    d.diem = float(diem)
                    self.show_score()
                    messagebox.showinfo("OK", "Sửa điểm thành công!")
                    return
                except:
                    messagebox.showerror("Lỗi", "Điểm phải là số!")
                    return
        messagebox.showerror("Lỗi", "Không tìm thấy môn này!")

    def delete_score(self):
        masv = self.masv2.get()
        mon = self.mon.get()
        lan = self.lan.get()
        if masv not in self.ds_diem:
            messagebox.showerror("Lỗi", "Chưa có điểm để xóa!")
            return
        for d in self.ds_diem[masv]:
            if d.mon == mon and d.lan == lan:
                self.ds_diem[masv].remove(d)
                self.show_score()
                messagebox.showinfo("OK", "Xóa điểm thành công!")
                return
        messagebox.showerror("Lỗi", "Không tìm thấy môn này!")

root = tk.Tk()
app = App(root)
root.mainloop()
