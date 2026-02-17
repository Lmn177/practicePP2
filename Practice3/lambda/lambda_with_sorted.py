students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)


words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)


users = [
    {"name": "Ivan", "age": 25},
    {"name": "Anna", "age": 20},
    {"name": "Oleg", "age": 30}
]


sorted_users = sorted(users, key=lambda user: user["age"])

print(sorted_users)