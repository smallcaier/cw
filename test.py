
import random
lst = [i for i in range(100)]

c = 0
l = []
while c <10:
    n = random.randint(0,100)
    l.append(lst[n])
    c += 1

print(l)
# print(n)
