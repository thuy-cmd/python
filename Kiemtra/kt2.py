import tkinter as tk
from tkinter import ttk, messagebox

def add_to_listbox(event=None):
    listbox.delete(0, tk.END)

    raw = entry_input.get().strip()
    if not raw:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, "Chưa nhập dãy số.")
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
        tk.messagebox.showwarning(
            "Giá trị không hợp lệ",
            f"Các mục sau không phải số nguyên: {', '.join(bad)}"
        )

    for n in nums:
        listbox.insert(tk.END, str(n))

    entry_input.delete(0, tk.END)
    entry_output.delete(0, tk.END)
    entry_output.insert(0, f"Đã thêm {len(nums)} số vào danh sách.")

def find_min():
    if listbox.size() == 0:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, "Danh sách rỗng.")
        return

    min_value = None
    for i in range(listbox.size()):
        try:
            num = int(listbox.get(i))
            if min_value is None or num < min_value:
                min_value = num
        except ValueError:
            pass

    entry_output.delete(0, tk.END)
    entry_output.insert(0, f"Số nhỏ nhất là: {min_value}")

def find_max():
    if listbox.size() == 0:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, "Danh sách rỗng.")
        return

    max_value = None
    for i in range(listbox.size()):
        try:
            num = int(listbox.get(i))
            if max_value is None or num > max_value:
                max_value = num
        except ValueError:
            pass

    entry_output.delete(0, tk.END)
    entry_output.insert(0, f"Số lớn nhất là: {max_value}")

def find_avg():
    if listbox.size() == 0:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, "Danh sách rỗng.")
        return

    numbers = []
    for i in range(listbox.size()):
        try:
            num = float(listbox.get(i))
            numbers.append(num)
        except ValueError:
            pass

    if len(numbers) == 0:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, "Không có số hợp lệ để tính trung bình.")
        return

    avg_value = sum(numbers) / len(numbers)

    for num in numbers:
        if num == avg_value:
            entry_output.delete(0, tk.END)
            entry_output.insert(0, f"Số trung bình là {avg_value}")
            return
        else:
            closest = sorted(numbers, key=lambda x: abs(x - avg_value))[:2]
            entry_output.delete(0, tk.END)
            entry_output.insert(0, f"Số gần với trung bình nhất là {closest[0]} và {closest[1]}")

def reset_form():
    entry_input.delete(0, tk.END)
    entry_output.delete(0, tk.END)
    listbox.delete(0, tk.END)

root = tk.Tk()
root.title("Form 1")
root.geometry("600x300")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.columnconfigure(2, weight=1)
frame.columnconfigure(3, weight=1)
frame.rowconfigure(2, weight=1)

label_input = ttk.Label(frame, text="Nhập: ")
label_input.grid(row=0, column=0, pady=10)
entry_input = ttk.Entry(frame)
entry_input.grid(row=0, column=1, padx=10, pady=10)

label_output = ttk.Label(frame, text="Kết quả: ")
label_output.grid(row=0, column=2, pady=10)
entry_output = ttk.Entry(frame, width=40)
entry_output.grid(row=0, column=3, padx=10, pady=10)

label_list = ttk.Label(frame, text="Dãy đã nhập: ")
label_list.grid(row=1, column=0, padx=10, pady=10)

listbox = tk.Listbox(frame)
listbox.grid(row=2, column=0, columnspan=3, rowspan=4, padx=10, pady=10, sticky="nsew")

button_min = ttk.Button(frame, text="Tìm Min", command=find_min)
button_min.grid(row=2, column=3, padx=10, pady=10)

button_max = ttk.Button(frame, text="Tìm Max", command=find_max)
button_max.grid(row=3, column=3, padx=10, pady=10)

button_avg = ttk.Button(frame, text="Tìm số TB", command=find_avg)
button_avg.grid(row=4, column=3, padx=10, pady=10)

button_reset = ttk.Button(frame, text="Làm lại", command=reset_form)
button_reset.grid(row=5, column=3, padx=10, pady=10)

entry_input.bind("<Return>", add_to_listbox)

root.mainloop()
