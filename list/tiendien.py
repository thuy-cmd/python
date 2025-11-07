tiendien = [int(i) for i in input().split()]

tongtien = sum(tiendien)
trungbinh = tongtien / 12

print(f"\nTong tien dien cua nam la: {tongtien}")
print(f"Tien dien trung binh cac thang la: {round(trungbinh, 2)}")
print("Cac thang co tien dien cao hon trung binh la: ")
for i in range(len(tiendien)):
    if tiendien[i] > trungbinh:
        print(f"+ Thang {i + 1}, tien dien: {tiendien[i]}")
