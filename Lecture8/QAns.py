#Let's Practice Some Exercises

#Q1. Create a student class that takes name & marks of 3 subjects as aruguements in constructor. Then create a method to print the average.
class Student:
    def __init__(self, name, marks): #Marks = [99, 98, 97]
        self.name = name
        self.marks = marks
    def hello():
        print("Hello!")
    def get_avg(self):
        sum = 0
        for val in self.marks:
            sum += val
        print("Hi", self.name,"Your average score is:", sum/len(self.marks))
s1 = Student("Tony Stark", [99, 98, 97])
s1.get_avg()

s1.name = "IronMan"
s1.get_avg()

#Q2. Create Account Class with 2 Attributes—Balance and Account Number. Create Methods for Debit, Credit & Printing the Balance.
class Account:
    def __init__(self, bal, acc_num):
        self.balance = bal
        self.account_number = acc_num
    #Debit method
    def debit(self, amount):
        self.balance -= amount
        print("₹", amount, "was debited from your account.")
        print("Total Balance =", self.get_balance())
    #Credit Method
    def credit(self, amount):
        self.balance += amount
        print("₹", amount, "was credited from your account.")
        print("Total Balance =", self.get_balance())
    #Final Balance Finding Method
    def get_balance(self):
        return self.balance

acc1 = Account(10000, 12345)
acc1.debit(1000)
acc1.credit(500)
acc1.credit(40000)
acc1.debit(10000)
print(acc1.balance)
print(acc1.account_number)

#Q3. Define a Circle class to create a circle with radius 'r' using the constructor. Define an Area() method of the class which calculates the area of the circle. Define a Perimeter() method of the class which allows you to calculate the perimeter of the circle.
class Circle:
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return (22/7) * self.radius ** 2
    def perimeter(self):
        return 2 * (22/7) * self.radius

c1 = Circle(float(input("Enter a radius: ")))
print(c1.area())
print(c1.perimeter())

#Q4. Define a Employee class with attribute roles, department & salary. This class also has a showDetails() method. Create an Engineer class that inherits properties from Employee & has additional attributes: Name and Age.
class Employee:
    def __init__(self, role, dept, salary):
        self.role = role
        self.dept = dept
        self.salary = salary
    def showDetails(self):
        print("role =", self.role)
        print("dept =", self.dept)
        print("salary =", self.salary)

class Engineer(Employee):
    def __init__(self, name, age):
        self.name = name
        self.age = age
        super().__init__("Engineer", "IT", "75,000")

e1 = Employee("Accountant", "Finance", "60,000")
e1.showDetails()

engg1 = Engineer("Elon Musk", 40)
engg1.showDetails()

#Q5. Create a class called Order which stores item & its price. Use Dunder function __gt__() to convey that. Order1 > Order2 If price of Order1 > Price of Order2
class Order:
    def __init__(self, item, price):
        self.item = item
        self.price = price
    def __gt__(self, odr2):
        return self.price > odr2.price

odr1 = Order("chips", 20)
odr2 = Order("tea", 15)
print(odr1 > odr2) #True

#If comment out Ln 89 & 90, an error will come. A TypeError: '>' not supported between instances of 'Order' and 'Order'.