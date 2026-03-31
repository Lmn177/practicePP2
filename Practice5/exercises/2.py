import re

pattern = r"^ab{2,3}$"
text = input("Enter text: ")

if re.match(pattern, text):
    print("Match found")
else:
    print("No match")