import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

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


def show_products():
    listbox.delete(0, tk.END)
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT masp, tensp, congty, gia FROM products ORDER BY id DESC')
    products = cursor.fetchall()
    for product in products:
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
        entry_tensp.delete(0, tk.END)
        entry_congty.delete(0, tk.END)
        entry_gia.delete(0, tk.END)

        entry_masp.insert(0, product[0])
        entry_tensp.insert(0, product[1])
        entry_congty.insert(0, product[2])
        entry_gia.insert(0, str(product[3]))


def find_product():
    masp = entry_masp_tim.get().strip()
    if not masp:
        messagebox.showwarning(
            "Thiếu thông tin",
            "Vui lòng nhập mã sản phẩm để tìm kiếm."
        )
        return
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute(
        'SELECT masp, tensp, congty, gia FROM products WHERE masp = ?', (masp,))
    product = cursor.fetchone()
    if product:
        entry_masp.delete(0, tk.END)
        entry_tensp.delete(0, tk.END)
        entry_congty.delete(0, tk.END)
        entry_gia.delete(0, tk.END)
        entry_masp.insert(0, product[0])
        entry_tensp.insert(0, product[1])
        entry_congty.insert(0, product[2])
        entry_gia.insert(0, str(product[3]))
        for i in range(listbox.size()):
            if listbox.get(i) == masp:
                listbox.selection_clear(0, tk.END)
                listbox.selection_set(i)
                listbox.see(i)
                break
    else:
        messagebox.showinfo(
            "Không tìm thấy", f"Sản phẩm với mã {masp} không tồn tại.")
    conn.close()


def delete_product():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    selected = listbox.curselection()
    isDelete = False
    if not selected:
        messagebox.showwarning("Lỗi", "Vui lòng chọn sản phẩm để xóa.")
        return

    isDelete = messagebox.askyesno(
        "Xác nhận", "Bạn có chắc chắn muốn xóa sản phẩm này không?")
    if not isDelete:
        conn.close()
        return
    else:
        masp = listbox.get(selected[0]).strip()
        cursor.execute('DELETE FROM products WHERE masp = ?', (masp,))
        conn.commit()
        conn.close()
        messagebox.showinfo(
            "Thành công", "Đã xóa sản phẩm khỏi cơ sở dữ liệu.")
        entry_masp.delete(0, tk.END)
        entry_tensp.delete(0, tk.END)
        entry_congty.delete(0, tk.END)
        entry_gia.delete(0, tk.END)
        show_products()


def calculate_total_price():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(gia) FROM products')
    total = int(cursor.fetchone()[0])
    conn.close()
    entry_sum.delete(0, tk.END)
    entry_sum.insert(0, str(total) if total is not None else "0")


def add_product():
    masp = entry_masp.get().strip()
    tensp = entry_tensp.get().strip()
    congty = entry_congty.get().strip()
    gia_str = entry_gia.get().strip()

    if not masp or not tensp or not congty or not gia_str:
        messagebox.showwarning(
            "Thiếu thông tin",
            "Vui lòng nhập đầy đủ thông tin sản phẩm."
        )
        show_products()
        return

    try:
        gia = float(gia_str)
    except ValueError:
        messagebox.showwarning(
            "Giá trị không hợp lệ",
            "Giá sản phẩm phải là một số hợp lệ."
        )
        show_products()
        return

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO products (masp, tensp, congty, gia) VALUES (?, ?, ?, ?)',
                       (masp, tensp, congty, gia))
        conn.commit()
        messagebox.showinfo(
            "Thành công", "Đã thêm sản phẩm vào cơ sở dữ liệu.")
    except sqlite3.IntegrityError:
        messagebox.showwarning("Lỗi", "Mã sản phẩm đã tồn tại.")
    finally:
        conn.close()

    entry_masp.delete(0, tk.END)
    entry_tensp.delete(0, tk.END)
    entry_congty.delete(0, tk.END)
    entry_gia.delete(0, tk.END)
    show_products()


root = tk.Tk()
root.title("Quản lý sản phẩm")
root.geometry("600x500")

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

frame_list = ttk.Frame(root, padding="10")
frame_list.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

frame_list.rowconfigure(1, weight=1)
frame_list.rowconfigure(0, weight=0)
frame_list.columnconfigure(0, weight=1)

frame_input = ttk.Frame(root, padding="10")
frame_input.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

for c in range(5):
    frame_input.rowconfigure(c, weight=1)
frame_input.columnconfigure(1, weight=1)

frame_controls = ttk.Frame(root, padding="10")
frame_controls.grid(row=1, column=0, columnspan=2,
                    sticky="ew", padx=10, pady=10)

frame_controls.columnconfigure(0, weight=1)
frame_controls.columnconfigure(1, weight=1)

label_list = ttk.Label(frame_list, text="Danh sách sản phẩm:")
label_list.grid(row=0, column=0, pady=10)

listbox = tk.Listbox(frame_list, height=15)
listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
listbox.bind('<<ListboxSelect>>', show_selected_product)

label_form = ttk.Label(frame_input, text="Nhập thông tin sản phẩm:")
label_form.grid(row=0, column=0, columnspan=2, pady=10)

label_masp = ttk.Label(frame_input, text="Mã sản phẩm:")
label_masp.grid(row=1, column=0, pady=10)
entry_masp = ttk.Entry(frame_input)
entry_masp.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

label_tensp = ttk.Label(frame_input, text="Tên sản phẩm:")
label_tensp.grid(row=2, column=0, pady=10)
entry_tensp = ttk.Entry(frame_input)
entry_tensp.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

label_congty = ttk.Label(frame_input, text="Công ty sản xuất:")
label_congty.grid(row=3, column=0, pady=10)
entry_congty = ttk.Entry(frame_input)
entry_congty.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

label_gia = ttk.Label(frame_input, text="Giá sản phẩm:")
label_gia.grid(row=4, column=0, pady=10)
entry_gia = ttk.Entry(frame_input)
entry_gia.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

button_add = ttk.Button(
    frame_controls, text="Thêm sản phẩm", command=add_product)
button_add.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

button_delete = ttk.Button(
    frame_controls, text="Xóa sản phẩm", command=delete_product)
button_delete.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

button_tim = ttk.Button(
    frame_controls, text="Tìm sản phẩm theo mã", command=find_product)
button_tim.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
entry_masp_tim = ttk.Entry(frame_controls)
entry_masp_tim.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

button_sum = ttk.Button(
    frame_controls, text="Tổng giá sản phẩm", command=calculate_total_price)
button_sum.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
entry_sum = ttk.Entry(frame_controls)
entry_sum.grid(row=1, column=1, padx=10, pady=10, sticky="ew", columnspan=3)

show_products()

root.mainloop()
