class Employee:
   
    company_name = "TechCorp"
    employee_count = 0

    def __init__(self, name):
       
        self.name = name
      
        Employee.employee_count += 1

emp1 = Employee("Alice")
emp2 = Employee("Bob")

print(f"Компания: {emp1.company_name}") 
print(f"Всего сотрудников: {Employee.employee_count}") 