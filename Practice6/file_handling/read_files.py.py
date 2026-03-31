# Task 1: Create a text file and write sample data
# Task 3: Append new lines and verify content
data = """Alice, 25, Engineer
Bob, 30, Designer
Charlie, 22, Artist"""

with open("sample.txt", "w") as f:
    f.write(data)

with open("sample.txt", "a") as f:
    f.write("\nDavid, 28, Analyst")