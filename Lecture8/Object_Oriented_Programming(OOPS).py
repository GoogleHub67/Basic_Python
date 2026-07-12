#Sample Show
a = 10
b = 20
sum = a + b
print(sum)
diff = a - b
print(diff)

list = ["Aarav", 94.4]

#Class and Object
class Student: #No INIT Functionn, Constructor will get executed
    def __init__(self):
        print("Adding New Student in Database...")
    name = "Aarav"
s1 = Student()
print(s1)
print(s1.name)
s2 = Student()
print(s2.name)

class Student:
    def __init__(self, name, marks):
        pass
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks
        print("Adding New Student in Database...")
s1 = Student("Karan", 97)
print(s1.name, s1.marks)
s2 = Student("Arjun", 88)
print(s2.name, s2.marks)
#You can use any other name instead of self, but "self" is mostly used.

class Car:
    color = "Blue"
    brand = "Mercedes"
car1 = Car()
print(car1.color)
print(car1.brand)
car2 = Car() #Constructor Executed