lst = [int(i) for i in input().split()]
v = int(input("Nhap so can tim: "))

if v in lst:
    print(f"So {v} xuat hien tai vi tri {lst.index(v) + 1} trong danh sach")
else:
    print(f"So {v} khong xuat hien trong danh sach")
