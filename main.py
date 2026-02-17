data = [10, "Привет", 3.14, 55, False, 100]
for x in data:
    if isinstance(x, int):
        print(x)


n = 123456789
m = 0
n = str(abs(int(n)))
for x in n:
    digit = int(x)
    if digit % 2 == 0:
        m = m + digit

print(m)

def is_empty(value):
    if bool(value):
        print("YES")
    else:
        print("NO")

is_empty(12354)
is_empty("dfgh")
is_empty(0)





def isUsual(num):
    if num <= 0:
        return False
    
    while num % 2 == 0:
        num //=2


    while num % 3 == 0:
        num //=3

    while num % 5 == 0:
        num //=5


    return num == 1


n = int(input())

if isUsual(n):
    print("Yes")
else:
    print("No")