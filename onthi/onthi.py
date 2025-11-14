import tkinter as tk
from tkinter import ttk, messagebox

def add_to_listbox(event=None):
    listbox.delete(0, tk.END)

    row = entry_input.get().strip()
    if not row:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, "Chưa nhập dãy số.")
        return

    tokens = row.split(',')

    nums, bad = [], []
    for t in tokens:
        if t == "":
            continue
        try:
            nums.append(int(t))
        except ValueError:
            bad.append(t)
    if bad:
        messagebox.showwarning(
            "Giá trị không hợp lệ",
            f"Các mục sau không phải số nguyên: {', '.join(bad)}"
        )
    for n in nums:
        listbox.insert(tk.END, str(n))
    entry_input.delete(0, tk.END)
    entry_output.delete(0, tk.END)
    entry_output.insert(0, f"Đã thêm {len(nums)} số vào danh sách.")


root = tk.Tk()
root.title("Form 1")
root.geometry("600x400")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

frame.columnconfigure(1, weight=1)
frame.columnconfigure(3, weight=1)

label_input = ttk.Label(frame, text="Nhập số: ")
label_input.grid(row=0, column=0, pady=10)
entry_input = ttk.Entry(frame)
entry_input.grid(row=0, column=1, padx=10, pady=10, sticky="ew", columnspan=1)

label_boisonhap = ttk.Label(frame, text="Bội/Ước của số: ")
label_boisonhap.grid(row=0, column=2, pady=10)
entry_input_boinhap = ttk.Entry(frame)
entry_input_boinhap.grid(row=0, column=3, padx=10, pady=10, sticky="ew", columnspan=1)

label_ketqua = ttk.Label(frame, text="Kết quả: ")
label_ketqua.grid(row=1, column=0, pady=10)
entry_output = ttk.Entry(frame)
entry_output.grid(row=1, column=1, padx=10, pady=10, sticky="ew", columnspan=3)

label_list = ttk.Label(frame, text="Dãy đã nhập: ")
label_list.grid(row=2, column=0, padx=10, pady=10)

listbox = tk.Listbox(frame, height=10)
listbox.grid(row=3, column=0, columnspan=3, rowspan=4, sticky="nsew", padx=10, pady=10)

button_add = ttk.Button(frame, text="Thêm số vào dãy", command=add_to_listbox)
button_add.grid(row=3, column=3, padx=10, pady=10, sticky="ew", columnspan=1)

button_boi = ttk.Button(frame, text="Tìm bội số")
button_boi.grid(row=4, column=3, padx=10, pady=10, sticky="ew", columnspan=1)

button_uoc = ttk.Button(frame, text="Tìm ước số")
button_uoc.grid(row=5, column=3, padx=10, pady=10, sticky="ew", columnspan=1)

button_exit = ttk.Button(frame, text="Thoát", command=root.destroy)
button_exit.grid(row=6, column=3, padx=10, pady=10, sticky="ew", columnspan=1)

entry_input.bind("<Return>", add_to_listbox)

root.mainloop()
