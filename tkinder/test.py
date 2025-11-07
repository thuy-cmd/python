
import tkinter as tk
from tkinter import ttk, Listbox, messagebox

def add_to_listbox(event=None):
    list_box.delete(0, tk.END)

    raw = entry_numbers.get().strip()
    if not raw:
        label_result.config(text="Chưa nhập dãy số.")
        return

    tokens = raw.split(',')

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

    entry_numbers.delete(0, tk.END)
    label_result.config(text=f"Đã thêm {len(nums)} số vào danh sách.")
def find_number(event=None):
    target_raw = entry_target.get().strip()
    if target_raw == "":
        label_result.config(text="Chưa nhập số cần tìm.")
        return
    try:
        target = int(target_raw)
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập một số nguyên hợp lệ.")
        return

    positions_0 = []
    for i in range(list_box.size()):
        try:
            if int(list_box.get(i)) == target:
                positions_0.append(i)
        except ValueError:
            pass

    list_box.selection_clear(0, tk.END)
    for i in positions_0:
        list_box.selection_set(i)
        list_box.see(i)

    if positions_0:
        positions_1 = [p + 1 for p in positions_0]
        label_result.config(
            text=f"Số {target} xuất hiện tại vị trí (bắt đầu từ 1): {', '.join(map(str, positions_1))}"
        )
    else:
        label_result.config(text=f"Số {target} không có trong danh sách.")

root = tk.Tk()
root.title("Tim vi tri xuat hien cua mot so trong day so nguyen")
root.geometry("520x380")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

frame = ttk.Frame(root, padding=12)
frame.grid(row=0, column=0, sticky="nsew")
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=0)

for r in range(6):
    frame.rowconfigure(r, weight=0)
frame.rowconfigure(6, weight=1)
ttl_label = ttk.Label(frame, text="Nhap day so nguyen (cach nhau boi dau phay):")
ttl_label.grid(row=0, column=0, sticky="w", columnspan=2)
entry_numbers = ttk.Entry(frame)
entry_numbers.grid(row=1, column=0, sticky="ew", pady=6, padx=(0, 8))
btn_add = ttk.Button(frame, text="Them vao Listbox", command=add_to_listbox)
btn_add.grid(row=1, column=1)
ttk.Label(frame, text="Danh sach so nguyen:").grid(row=2, column=0, sticky="w", columnspan=2)
list_box = Listbox(frame, height=10)
list_box.grid(row=3, column=0, columnspan=2, sticky="nsew")
ttk.Label(frame, text="Nhap so can tim:").grid(row=4, column=0, sticky="w", columnspan=2, pady=(10, 0))
entry_target = ttk.Entry(frame)
entry_target.grid(row=5, column=0, sticky="ew", pady=6, padx=(0, 8))
btn_find = ttk.Button(frame, text="Tim so", command=find_number)
btn_find.grid(row=5, column=1)
label_result = ttk.Label(frame, text="")
label_result.grid(row=6, column=0, columnspan=2, sticky="w", pady=(10, 0))

button_exit = ttk.Button(frame, text="Thoat", command=root.destroy)
button_exit.grid(row=7, column=0, columnspan=2, pady=(20, 0))

btn_add.bind("<Return>", add_to_listbox)
btn_find.bind("<Return>", find_number)
root.mainloop()
