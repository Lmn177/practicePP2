# task 1
import math
degree = float(input("Inpur degree: "))
radian = degree * (math.pi / 180)
print("Outpur radian:", round(radian,6))

import math
degree = float(input("Input degree: "))
radian = math.radians(degree)
print("Output radian:", round(radian, 6))

#task 2
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))

area = ((base1 + base2)/2 * height)
print("Area:",area)