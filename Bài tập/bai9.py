s = 'hsg8ngay21thang4nam2023'
sum = 0
res = ''
a = ''
b = 0
for char in s:
    if char.isdigit():
        a += char
        res += char
    else:
        if (res):
            sum += int(res)
            res = ''
if (res):
    sum += int(res)

for i in range(len(a) - 1, -1, -1):
    if (a[i] in '05'):
        b = int(a[:i+1])
    
print(a)
print(b)
print(sum)
