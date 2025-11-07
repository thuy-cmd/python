lst = input().split()
cnt = 0

for i in lst:
    if i.isdigit():
        if int(i) % 2 == 0:
            cnt += 1

print(f"Trong danh sach co {cnt} phan tu chan")
