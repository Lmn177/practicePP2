class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Emil", 36)

print(p1.name)
print(p1.age)



class Person:
  pass

p1 = Person()
p1.name = "Tobias"
p1.age = 25

print(p1.name)
print(p1.age)




class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Linus", 28)

print(p1.name)
print(p1.age)



class Person:
  def __init__(self, name, age=18):
    self.name = name
    self.age = age

p1 = Person("Emil")
p2 = Person("Tobias", 25)

print(p1.name, p1.age)
print(p2.name, p2.age)




class Person:
  def __init__(self, name, age, city, country):
    self.name = name
    self.age = age
    self.city = city
    self.country = country

p1 = Person("Linus", 30, "Oslo", "Norway")

print(p1.name)
print(p1.age)
print(p1.city)
print(p1.country)


class BankAccount:
    bank_name = "Python Bank"  

    def __init__(self, owner, balance=0):
        self.owner = owner     
        self.balance = balance 

    def deposit(self, amount):
        self.balance += amount
        print(f"{self.owner}, вы внесли {amount}. Баланс: {self.balance}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Снято {amount}. Остаток: {self.balance}")
        else:
            print("Недостаточно средств!")

acc = BankAccount("Dmitry", 1000)
acc.deposit(500)
acc.withdraw(200)