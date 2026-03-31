from functools import reduce

names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 22]

# Task 1 & 2: map, filter, and reduce
upper_names = list(map(str.upper, names))
adults = list(filter(lambda x: x > 24, ages))
total_age = reduce(lambda x, y: x + y, ages)

print(f"Upper: {upper_names}\nAdults: {adults}\nTotal Age: {total_age}")