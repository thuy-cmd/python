import tkinter as tk
from tkinter import ttk, Listbox, messagebox

def add_to_listbox(event=None):
    list_box.delete(0, tk.END)

    row = entry_input.get().strip()
    if not row:
        label_result.config(text="Chưa nhập dãy số.")
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
        list_box.insert(tk.END, str(n))

    entry_input.delete(0,tk.END)
    label_result.config(text=f"Đã thêm {len(nums)} số vào danh sách.")

def find_number(event=None):
    target_row = entry_target.get().strip()
    if target_row == "":
        label_result.config(text="Chưa nhập số cần tìm.")
        return
    try:
        target = int(target_row)
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên hợp lệ.")
        return
    possition_before = []
    for i in range(list_box.size()):
        try:
            if (int(list_box.get(i))) == target:
                possition_before.append(i)
        except ValueError:
            pass
    list_box.selection_clear(0, tk.END)
    for i in possition_before:
        list_box.selection_set(i)
        list_box.see(i)

    if possition_before:
        possition_after = [p + 1 for p in possition_before]
        res = f"Số {target} xuất hiện ở các vị trí: " + ", ".join(map(str, possition_after))
    else:
        res = f"Số {target} không xuất hiện trong dãy."
    label_result.config(text=res )

root = tk.Tk()
root.title("Tìm vị trí xuất hiện của một số trong dãy số nguyên")
root.geometry("520x380")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

frame = ttk.Frame(root, padding=12)
frame.grid(row=0, column=0, sticky="nsew")

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=0)

for i in range(7):
    frame.rowconfigure(i, weight=0)
frame.rowconfigure(3, weight=1)

label_input = ttk.Label(frame, text="Nhập danh sách số nguyên (cách nhau bởi dấu phẩy)")
label_input.grid(row=0, column=0, sticky="w", columnspan=2)

entry_input = ttk.Entry(frame)
entry_input.grid(row=1, column=0, sticky="ew", pady=6, padx=(0, 8))

btn_add = ttk.Button(frame, text="Add to Listbox", command=add_to_listbox)
btn_add.grid(row=1, column=1)

label_list = ttk.Label(frame, text="Danh sách số nguyên: ")
label_list.grid(row=2, column=0, sticky="w")

list_box = Listbox(frame, height=10)
list_box.grid(row=3, column=0, sticky="nsew", columnspan=2, pady=6)

label_target = ttk.Label(frame, text="Nhập số cần tìm: ")
label_target.grid(row=4, column=0, sticky="w")

entry_target = ttk.Entry(frame)
entry_target.grid(row=5, column=0, sticky="ew", pady=6, padx=(0, 8))

btn_find = ttk.Button(frame, text="Tìm số", command=find_number)
btn_find.grid(row=5, column=1)

label_result = ttk.Label(frame, text="So can tim", background="#5ebbff", wraplength=480, justify="left", font=16)
label_result.grid(row=6, column=0, columnspan=2, sticky="w", pady=6)

btn_exit = ttk.Button(frame, text="Thoát", command=root.destroy)
btn_exit.grid(row=7, column=0, columnspan=3, pady=6, sticky="e")

entry_input.bind("<Return>", add_to_listbox)
entry_target.bind("<Return>", find_number)

root.mainloop()
