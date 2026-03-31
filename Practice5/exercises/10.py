import re

def camel_to_snake(s):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

text = input("Enter camelCase text: ")
print("snake_case:", camel_to_snake(text))