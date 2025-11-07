
str1 = input("Nhap chuoi: ")
str2 = str1.split(" ")
res = ''

for txt in str2:
    res += txt[0].upper() + txt[1:] + ' '
    
print(res.strip())
