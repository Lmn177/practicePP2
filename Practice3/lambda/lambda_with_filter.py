numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)


numbers = [1, 5, 4, 6, 8, 11, 3, 12]


even_numbers = list(filter(lambda x: x % 2 == 0, numbers))

print(even_numbers) 