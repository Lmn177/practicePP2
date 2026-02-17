numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

prices = [100, 250, 400, 150]


prices_with_tax = list(map(lambda p: p * 1.1, prices))

print(prices_with_tax) 