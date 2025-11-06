def common_divisor(x, y):
    if y == 0:
        return x
    else:
        return common_divisor(y, x % y)

a, b, total, n = 1009, 3643, 0, 3
t = (a - 1) * (b - 1)
while n < t:
    if common_divisor(n, t) == 1 and common_divisor(n - 1, b - 1) == 2 and common_divisor(n - 1, a - 1) == 2:
        total += n
    n += 2

print(total)
