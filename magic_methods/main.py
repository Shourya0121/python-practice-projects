class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"Student: {self.name}, Age {self.age}"

student = Student("shourya", 21)

print(student)

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product: {self.name}, {self.price}"

product = Product("laptop", 35000)
print(product)

class Team:
    def __init__(self,players):
        self.players = players

    def __len__(self):
        return len(self.players)

team = Team(["Rhaul", "Amit", "Puran"])
print(len(team))

class BankAccount:
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance

    def __eq__(self, others):
        return self.account_number == others.account_number

account1 = BankAccount(101, 5000)
account2 = BankAccount(101, 5000)
print(account1 == account2)
