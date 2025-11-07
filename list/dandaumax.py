lst = [int(i) for i in input().split()]

for num in lst:
    print(num, end=' ')

max_length = cur_length = 1
l = r = 0
cur_l = 0
print(len(lst))

for i in range(1,len(lst)):
    if (lst[i] * lst[i - 1]) < 0:
        cur_length += 1
    else:
        cur_length = 1
        cur_l = i

    if (cur_length > max_length):
        max_length = cur_length
        l = cur_l
        r = i
print()
print(max_length)
for i in range(l, r + 1):
    print(lst[i], end=' ')
