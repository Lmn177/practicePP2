class MyClass:
  x = 5

p1 = MyClass()
print(p1.x)

p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)



class Car:
    def __init__(self, model, color):
        self.model = model
        self.color = color

c1 = Car("Tesla", "Red")

c1.color = "Black"

del c1.color 

