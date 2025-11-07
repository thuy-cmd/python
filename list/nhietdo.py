nhietdo = [float(i) for i in input().split()]

print("Cac ngay co nhiet do duoi 10 la: ", end='')
for i in range(7):
    if nhietdo[i] < 10:
        if i == 6:
            print("CN", end="")
        else:
            print(f"thu {i + 2}", end=" ")
    
print(".")
print(f"Ngay co nhiet do cao nhat la {max(nhietdo)}")
print(f"Ngay co nhiet do thap nhat la {min(nhietdo)}")