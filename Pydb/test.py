import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ============================
# TẠO STYLE LUNG LINH
# ============================


def apply_style(root, dark=True):
    style = ttk.Style(root)

    if dark:
        bg = "#1e1e1e"
        fg = "white"
        entry_bg = "#2b2b2b"
        button_bg = "#3a3a3a"
        list_bg = "#2d2d2d"
    else:
        bg = "#020101"
        fg = "black"
        entry_bg = "white"
        button_bg = "#e6e6e6"
        list_bg = "white"

    root.configure(bg=bg)
    style.configure("TFrame", background=bg)
    style.configure("TLabelframe", background=bg,
                    foreground=fg, font=("Segoe UI", 12, "bold"))
    style.configure("TLabel", background=bg,
                    foreground=fg, font=("Segoe UI", 11))
    style.configure("TButton", font=("Segoe UI Semibold", 11), padding=6)
    style.map("TButton",
              background=[("active", "#4CAF50"), ("!active", button_bg)],
              foreground=[("active", "white")])

    style.configure("TEntry", padding=5,
                    fieldbackground=entry_bg, foreground=fg)
    style.configure("TCombobox", fieldbackground=entry_bg,
                    background=entry_bg, foreground=fg)

    root.list_bg = list_bg


# ============================
# CHUYỂN ĐỔI DARK/LIGHT MODE
# ============================
dark_mode = True


def toggle_mode():
    global dark_mode
    dark_mode = not dark_mode
    apply_style(root, dark_mode)
    listbox.config(bg=root.list_bg, fg="white" if dark_mode else "black")


# ============================
# DATABASE
# ============================
conn = sqlite3.connect('products.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        masp TEXT UNIQUE,
        tensp TEXT,
        congty TEXT,
        gia REAL
    )
''')
conn.commit()
conn.close()


# ============================
# CÁC HÀM XỬ LÝ
# ============================
def show_products():
    listbox.delete(0, tk.END)
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT masp, tensp, congty, gia FROM products ORDER BY id DESC')
    for product in cursor.fetchall():
        listbox.insert(tk.END, product[0])
    conn.close()


def show_selected_product(event):
    selected = listbox.curselection()
    if not selected:
        return
    masp = listbox.get(selected[0]).strip()
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT masp, tensp, congty, gia FROM products WHERE masp = ?', (masp,))
    product = cursor.fetchone()
    conn.close()
    if product:
        entry_masp.delete(0, tk.END)
        entry_masp.insert(0, product[0])
        entry_tensp.delete(0, tk.END)
        entry_tensp.insert(0, product[1])
        entry_congty.delete(0, tk.END)
        entry_congty.insert(0, product[2])
        entry_gia.delete(0, tk.END)
        entry_gia.insert(0, str(product[3]))


def find_product():
    masp = entry_masp_tim.get().strip()
    if not masp:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã sản phẩm!")
        return

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT masp, tensp, congty, gia FROM products WHERE masp = ?', (masp,))
    product = cursor.fetchone()
    conn.close()

    if product:
        entry_masp.delete(0, tk.END)
        entry_masp.insert(0, product[0])
        entry_tensp.delete(0, tk.END)
        entry_tensp.insert(0, product[1])
        entry_congty.delete(0, tk.END)
        entry_congty.insert(0, product[2])
        entry_gia.delete(0, tk.END)
        entry_gia.insert(0, str(product[3]))

        for i in range(listbox.size()):
            if listbox.get(i) == masp:
                listbox.selection_clear(0, tk.END)
                listbox.selection_set(i)
                listbox.see(i)
                break
    else:
        messagebox.showinfo(
            "Không tìm thấy", f"Sản phẩm mã {masp} không tồn tại.")


def delete_product():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Lỗi", "Hãy chọn sản phẩm để xóa.")
        return

    if not messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa?"):
        return

    masp = listbox.get(selected[0]).strip()

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE masp = ?', (masp,))
    conn.commit()
    conn.close()

    entry_masp.delete(0, tk.END)
    entry_tensp.delete(0, tk.END)
    entry_congty.delete(0, tk.END)
    entry_gia.delete(0, tk.END)

    show_products()
    messagebox.showinfo("Thành công", "Đã xóa sản phẩm.")


def calculate_total_price():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(gia) FROM products')
    total = cursor.fetchone()[0]
    conn.close()

    entry_sum.delete(0, tk.END)
    entry_sum.insert(0, str(total if total else 0))


def add_product():
    masp = entry_masp.get().strip()
    tensp = entry_tensp.get().strip()
    congty = entry_congty.get().strip()
    gia_str = entry_gia.get().strip()

    if not masp or not tensp or not congty or not gia_str:
        messagebox.showwarning("Thiếu thông tin", "Điền đầy đủ thông tin.")
        return

    try:
        gia = float(gia_str)
    except:
        messagebox.showwarning("Sai định dạng", "Giá phải là số.")
        return

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO products (masp, tensp, congty, gia) VALUES (?, ?, ?, ?)",
                       (masp, tensp, congty, gia))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showwarning("Trùng mã", "Mã sản phẩm đã tồn tại.")
        conn.close()
        return
    conn.close()

    entry_masp.delete(0, tk.END)
    entry_tensp.delete(0, tk.END)
    entry_congty.delete(0, tk.END)
    entry_gia.delete(0, tk.END)

    show_products()
    messagebox.showinfo("Thành công", "Đã thêm sản phẩm!")


# ============================
# GIAO DIỆN CHÍNH
# ============================
root = tk.Tk()
root.title("🌟 Quản lý sản phẩm – Giao diện nâng cấp 🌟")
root.geometry("700x600")

apply_style(root, True)

# Layout
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# --- Danh sách sản phẩm ---
frame_list = ttk.Labelframe(root, text="Danh sách sản phẩm", padding=10)
frame_list.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

frame_list.columnconfigure(0, weight=1)
frame_list.rowconfigure(1, weight=1)

listbox = tk.Listbox(frame_list, font=("Segoe UI", 12),
                     bg=root.list_bg, fg="white", selectbackground="#4CAF50")
listbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
listbox.bind("<<ListboxSelect>>", show_selected_product)

# --- Form nhập ---
frame_input = ttk.Labelframe(root, text="Thông tin sản phẩm", padding=10)
frame_input.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

frame_input.columnconfigure(1, weight=1)

labels = ["Mã sản phẩm:", "Tên sản phẩm:", "Công ty sản xuất:", "Giá:"]
entries = []

for i, text in enumerate(labels, start=1):
    ttk.Label(frame_input, text=text).grid(row=i, column=0, sticky="w", pady=5)
    entry = ttk.Entry(frame_input)
    entry.grid(row=i, column=1, sticky="ew", pady=5)
    entries.append(entry)

entry_masp, entry_tensp, entry_congty, entry_gia = entries

# --- Controls ---
frame_controls = ttk.Frame(root, padding=10)
frame_controls.grid(row=1, column=0, columnspan=2, sticky="ew")

for i in range(4):
    frame_controls.columnconfigure(i, weight=1)

ttk.Button(frame_controls, text="➕ Thêm", command=add_product).grid(
    row=0, column=0, padx=5, pady=5, sticky="ew")
ttk.Button(frame_controls, text="🗑 Xóa", command=delete_product).grid(
    row=0, column=1, padx=5, pady=5, sticky="ew")
ttk.Button(frame_controls, text="🔍 Tìm", command=find_product).grid(
    row=0, column=2, padx=5, pady=5, sticky="ew")

entry_masp_tim = ttk.Entry(frame_controls)
entry_masp_tim.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

ttk.Button(frame_controls, text="💰 Tổng giá", command=calculate_total_price).grid(
    row=1, column=0, padx=5, pady=5, sticky="ew")

entry_sum = ttk.Entry(frame_controls)
entry_sum.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

# Nút chuyển đổi theme
ttk.Button(frame_controls, text="🌗 Chế độ sáng / tối", command=toggle_mode).grid(row=2,
                                                                                 column=0, columnspan=4, padx=5, pady=10, sticky="ew")

# Load danh sách ban đầu
show_products()
root.mainloop()
