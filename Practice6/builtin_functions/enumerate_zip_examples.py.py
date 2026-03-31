names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 22]

# Task 3 & 4: enumerate, zip, and type checking
for i, (n, a) in enumerate(zip(names, ages)):
    print(f"ID {i}: {n} is {a}")

val = "500"
if isinstance(val, str):
    converted = int(val)
    print(f"Type changed from {type(val)} to {type(converted)}")