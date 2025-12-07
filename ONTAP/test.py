#!/usr/bin/env python3
"""
Student & Scores manager - Tkinter + SQLite (Procedural, no class)
Save as student_manager_proc.py and run: python student_manager_proc.py
"""
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_FILE = "students_proc.db"

# ---------- Global DB connection ----------
conn = None

def init_db():
    global conn
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS SinhVien (
            MaSV TEXT PRIMARY KEY,
            HoTen TEXT NOT NULL,
            Lop TEXT,
            NamSinh INTEGER
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS DiemThi (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            MaSV TEXT NOT NULL,
            Mon TEXT NOT NULL,
            Diem REAL,
            FOREIGN KEY (MaSV) REFERENCES SinhVien(MaSV) ON DELETE CASCADE
        );
    """)
    conn.commit()

# ---------- DB helper functions ----------
def all_students():
    cur = conn.cursor()
    cur.execute("SELECT MaSV, HoTen, Lop, NamSinh FROM SinhVien ORDER BY MaSV")
    return cur.fetchall()

def get_student(masv):
    cur = conn.cursor()
    cur.execute("SELECT MaSV, HoTen, Lop, NamSinh FROM SinhVien WHERE MaSV=?", (masv,))
    return cur.fetchone()

def search_students_db(kw):
    kwp = f"%{kw}%"
    cur = conn.cursor()
    cur.execute("SELECT MaSV, HoTen, Lop, NamSinh FROM SinhVien WHERE MaSV LIKE ? OR HoTen LIKE ? OR Lop LIKE ? ORDER BY MaSV", (kwp, kwp, kwp))
    return cur.fetchall()

def add_student_db(masv, hoten, lop, namsinh):
    try:
        conn.execute("INSERT INTO SinhVien (MaSV, HoTen, Lop, NamSinh) VALUES (?, ?, ?, ?)",
                     (masv, hoten, lop, namsinh))
        conn.commit()
        return True
    except Exception as e:
        return False

def update_student_db(masv, hoten, lop, namsinh):
    conn.execute("UPDATE SinhVien SET HoTen=?, Lop=?, NamSinh=? WHERE MaSV=?", (hoten, lop, namsinh, masv))
    conn.commit()

def delete_student_db(masv):
    conn.execute("DELETE FROM SinhVien WHERE MaSV=?", (masv,))
    conn.commit()

def scores_of_db(masv):
    cur = conn.cursor()
    cur.execute("SELECT ID, Mon, Diem FROM DiemThi WHERE MaSV=? ORDER BY ID", (masv,))
    return cur.fetchall()

def add_score_db(masv, mon, diem):
    conn.execute("INSERT INTO DiemThi (MaSV, Mon, Diem) VALUES (?, ?, ?)", (masv, mon, diem))
    conn.commit()

def update_score_db(sid, mon, diem):
    conn.execute("UPDATE DiemThi SET Mon=?, Diem=? WHERE ID=?", (mon, diem, sid))
    conn.commit()

def delete_score_db(sid):
    conn.execute("DELETE FROM DiemThi WHERE ID=?", (sid,))
    conn.commit()

# ---------- GUI / App ----------
def build_ui(root):
    root.title("Quản lý Sinh viên & Điểm thi (procedural)")
    root.geometry("900x520")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    notebook = ttk.Notebook(root)
    notebook.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

    # --- Tab Sinh viên ---
    tab_sv = ttk.Frame(notebook)
    notebook.add(tab_sv, text="Sinh viên")
    tab_sv.rowconfigure(0, weight=1)
    tab_sv.columnconfigure(1, weight=1)

    # Left listbox
    frame_left = ttk.Frame(tab_sv)
    frame_left.grid(row=0, column=0, sticky="ns", padx=(8,4), pady=8)
    ttk.Label(frame_left, text="Danh sách sinh viên").grid(row=0, column=0, sticky="w")
    lb_sv = tk.Listbox(frame_left, width=28, height=22, exportselection=False)
    lb_sv.grid(row=1, column=0, sticky="ns")
    sb1 = ttk.Scrollbar(frame_left, orient="vertical", command=lb_sv.yview)
    sb1.grid(row=1, column=1, sticky="ns")
    lb_sv.config(yscrollcommand=sb1.set)

    # Right form
    frame_right = ttk.Frame(tab_sv, padding=(6,0))
    frame_right.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
    for i in range(4):
        frame_right.rowconfigure(i, weight=0)
    frame_right.columnconfigure(1, weight=1)

    ttk.Label(frame_right, text="Mã SV:").grid(row=0, column=0, sticky="w", pady=4)
    e_masv = ttk.Entry(frame_right)
    e_masv.grid(row=0, column=1, sticky="we", pady=4)

    ttk.Label(frame_right, text="Họ tên:").grid(row=1, column=0, sticky="w", pady=4)
    e_hoten = ttk.Entry(frame_right)
    e_hoten.grid(row=1, column=1, sticky="we", pady=4)

    ttk.Label(frame_right, text="Lớp:").grid(row=2, column=0, sticky="w", pady=4)
    e_lop = ttk.Entry(frame_right)
    e_lop.grid(row=2, column=1, sticky="we", pady=4)

    ttk.Label(frame_right, text="Năm sinh:").grid(row=3, column=0, sticky="w", pady=4)
    e_namsinh = ttk.Entry(frame_right)
    e_namsinh.grid(row=3, column=1, sticky="w", pady=4)

    btn_frame = ttk.Frame(frame_right)
    btn_frame.grid(row=4, column=0, columnspan=2, pady=8, sticky="w")
    btn_add = ttk.Button(btn_frame, text="Thêm")
    btn_add.grid(row=0, column=0, padx=4)
    btn_edit = ttk.Button(btn_frame, text="Sửa")
    btn_edit.grid(row=0, column=1, padx=4)
    btn_delete = ttk.Button(btn_frame, text="Xóa")
    btn_delete.grid(row=0, column=2, padx=4)

    ttk.Label(btn_frame, text="Tìm:").grid(row=0, column=3, padx=(20,4))
    e_search = ttk.Entry(btn_frame, width=20)
    e_search.grid(row=0, column=4, padx=4)
    btn_search = ttk.Button(btn_frame, text="Tìm")
    btn_search.grid(row=0, column=5, padx=4)
    btn_refresh = ttk.Button(btn_frame, text="Tải lại")
    btn_refresh.grid(row=0, column=6, padx=4)

    # --- Tab Điểm thi ---
    tab_dt = ttk.Frame(notebook)
    notebook.add(tab_dt, text="Điểm thi")
    tab_dt.rowconfigure(0, weight=1)
    tab_dt.columnconfigure(1, weight=1)

    left_dt = ttk.Frame(tab_dt)
    left_dt.grid(row=0, column=0, sticky="ns", padx=(8,4), pady=8)
    ttk.Label(left_dt, text="Danh sách sinh viên").grid(row=0, column=0, sticky="w")
    lb_dt = tk.Listbox(left_dt, width=28, height=20, exportselection=False)
    lb_dt.grid(row=1, column=0, sticky="ns")
    sb2 = ttk.Scrollbar(left_dt, orient="vertical", command=lb_dt.yview)
    sb2.grid(row=1, column=1, sticky="ns")
    lb_dt.config(yscrollcommand=sb2.set)

    right_dt = ttk.Frame(tab_dt, padding=(6,0))
    right_dt.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
    right_dt.columnconfigure(0, weight=1)

    ttk.Label(right_dt, text="Danh sách điểm").grid(row=0, column=0, sticky="w")
    tree = ttk.Treeview(right_dt, columns=("id","mon","diem"), show="headings", height=10, selectmode="browse")
    tree.heading("id", text="ID")
    tree.heading("mon", text="Môn")
    tree.heading("diem", text="Điểm")
    tree.grid(row=1, column=0, sticky="nsew")
    # allow horizontal expand
    right_dt.rowconfigure(1, weight=1)

    form_dt = ttk.Frame(right_dt)
    form_dt.grid(row=2, column=0, sticky="w", pady=6)
    ttk.Label(form_dt, text="Môn:").grid(row=0, column=0, sticky="e", padx=4)
    e_mon = ttk.Entry(form_dt, width=30)
    e_mon.grid(row=0, column=1, sticky="w", padx=4)
    ttk.Label(form_dt, text="Điểm:").grid(row=1, column=0, sticky="e", padx=4)
    e_diem = ttk.Entry(form_dt, width=10)
    e_diem.grid(row=1, column=1, sticky="w", padx=4)

    btns_dt = ttk.Frame(right_dt)
    btns_dt.grid(row=3, column=0, sticky="w", pady=6)
    btn_add_score = ttk.Button(btns_dt, text="Thêm điểm")
    btn_add_score.grid(row=0, column=0, padx=4)
    btn_edit_score = ttk.Button(btns_dt, text="Sửa điểm")
    btn_edit_score.grid(row=0, column=1, padx=4)
    btn_delete_score = ttk.Button(btns_dt, text="Xóa điểm")
    btn_delete_score.grid(row=0, column=2, padx=4)
    btn_refresh_score = ttk.Button(btns_dt, text="Tải lại")
    btn_refresh_score.grid(row=0, column=3, padx=4)

    # ---------- Event callbacks ----------
    def load_students_ui():
        lb_sv.delete(0, tk.END)
        lb_dt.delete(0, tk.END)
        rows = all_students()
        for r in rows:
            lb_sv.insert(tk.END, r[0])
            lb_dt.insert(tk.END, r[0])
        clear_student_form()
        tree.delete(*tree.get_children())

    def on_select_sv(event=None):
        sel = lb_sv.curselection()
        if not sel:
            return
        masv = lb_sv.get(sel[0])
        sv = get_student(masv)
        if sv:
            e_masv.delete(0, tk.END)
            e_masv.insert(0, sv[0])
            e_hoten.delete(0, tk.END)
            e_hoten.insert(0, sv[1])
            e_lop.delete(0, tk.END)
            e_lop.insert(0, sv[2] if sv[2] else "")
            e_namsinh.delete(0, tk.END)
            e_namsinh.insert(0, str(sv[3]) if sv[3] else "")

    def add_student_ui():
        masv = e_masv.get().strip()
        hoten = e_hoten.get().strip()
        lop = e_lop.get().strip()
        ns = e_namsinh.get().strip() or None
        if not masv or not hoten:
            messagebox.showwarning("Thiếu dữ liệu", "Mã SV và Họ tên bắt buộc.")
            return
        ok = add_student_db(masv, hoten, lop, ns)
        if not ok:
            messagebox.showerror("Lỗi", "Mã SV đã tồn tại hoặc lỗi thêm.")
            return
        messagebox.showinfo("OK", "Đã thêm sinh viên.")
        load_students_ui()

    def edit_student_ui():
        masv = e_masv.get().strip()
        if not masv:
            messagebox.showwarning("Chọn SV", "Nhập hoặc chọn Mã SV.")
            return
        hoten = e_hoten.get().strip()
        lop = e_lop.get().strip()
        ns = e_namsinh.get().strip() or None
        update_student_db(masv, hoten, lop, ns)
        messagebox.showinfo("OK", "Đã cập nhật.")
        load_students_ui()

    def delete_student_ui():
        sel = lb_sv.curselection()
        if not sel:
            messagebox.showwarning("Chọn SV", "Chọn sinh viên để xóa.")
            return
        masv = lb_sv.get(sel[0])
        if messagebox.askyesno("Xác nhận", f"Xóa sinh viên {masv} và điểm liên quan?"):
            delete_student_db(masv)
            messagebox.showinfo("Đã xóa", "Đã xóa.")
            load_students_ui()

    def search_ui():
        kw = e_search.get().strip()
        if not kw:
            load_students_ui()
            return
        rows = search_students_db(kw)
        lb_sv.delete(0, tk.END)
        for r in rows:
            lb_sv.insert(tk.END, r[0])

    def clear_student_form():
        e_masv.delete(0, tk.END)
        e_hoten.delete(0, tk.END)
        e_lop.delete(0, tk.END)
        e_namsinh.delete(0, tk.END)

    # Scores callbacks
    def load_scores_ui(event=None):
        sel = lb_dt.curselection()
        if not sel:
            return
        masv = lb_dt.get(sel[0])
        rows = scores_of_db(masv)
        tree.delete(*tree.get_children())
        for r in rows:
            tree.insert("", tk.END, values=r)

    def add_score_ui():
        sel = lb_dt.curselection()
        if not sel:
            messagebox.showwarning("Chọn SV", "Chọn sinh viên ở cột trái trước.")
            return
        masv = lb_dt.get(sel[0])
        mon = e_mon.get().strip()
        diem = e_diem.get().strip()
        if not mon:
            messagebox.showwarning("Thiếu dữ liệu", "Nhập tên môn.")
            return
        try:
            diem_v = float(diem) if diem != "" else None
        except:
            messagebox.showwarning("Sai dữ liệu", "Điểm phải là số.")
            return
        add_score_db(masv, mon, diem_v)
        e_mon.delete(0, tk.END)
        e_diem.delete(0, tk.END)
        load_scores_ui()

    def on_tree_double(event=None):
        sel = tree.selection()
        if not sel:
            return
        item = tree.item(sel[0])
        sid, mon, diem = item['values']
        e_mon.delete(0, tk.END)
        e_mon.insert(0, mon)
        e_diem.delete(0, tk.END)
        e_diem.insert(0, str(diem) if diem is not None else "")

    def edit_score_ui():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chọn điểm", "Chọn bản ghi trong danh sách điểm.")
            return
        item = tree.item(sel[0])
        sid = item['values'][0]
        mon = e_mon.get().strip()
        diem = e_diem.get().strip()
        if not mon:
            messagebox.showwarning("Thiếu dữ liệu", "Nhập tên môn.")
            return
        try:
            diem_v = float(diem) if diem != "" else None
        except:
            messagebox.showwarning("Sai dữ liệu", "Điểm phải là số.")
            return
        update_score_db(sid, mon, diem_v)
        load_scores_ui()

    def delete_score_ui():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Chọn điểm", "Chọn bản ghi để xóa.")
            return
        sid = tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Xác nhận", "Xóa bản ghi điểm này?"):
            delete_score_db(sid)
            load_scores_ui()

    # ---------- wire events to widgets ----------
    lb_sv.bind("<<ListboxSelect>>", on_select_sv)
    btn_add.config(command=add_student_ui)
    btn_edit.config(command=edit_student_ui)
    btn_delete.config(command=delete_student_ui)
    btn_search.config(command=search_ui)
    btn_refresh.config(command=load_students_ui)

    lb_dt.bind("<<ListboxSelect>>", load_scores_ui)
    btn_add_score.config(command=add_score_ui)
    btn_edit_score.config(command=edit_score_ui)
    btn_delete_score.config(command=delete_score_ui)
    btn_refresh_score.config(command=load_scores_ui)
    tree.bind("<Double-1>", on_tree_double)

    # initial load
    load_students_ui()

# ---------- main ----------
def main():
    init_db()
    root = tk.Tk()
    build_ui(root)
    root.mainloop()
    if conn:
        conn.close()

if __name__ == "__main__":
    main()
