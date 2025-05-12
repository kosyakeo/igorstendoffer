j = input().strip()
s = input().strip()
jewels = set(j)
count = 0
for char in s:
    if char in jewels:
        count += 1
print(count)