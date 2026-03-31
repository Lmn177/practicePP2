import re

text = input("Enter text: ")
result = re.findall(r'[A-Z][^A-Z]*', text)

print("Split result:", result)