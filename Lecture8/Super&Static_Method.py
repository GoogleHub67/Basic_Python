class Car:
    def __init__(self, type):
        self.type = type
    color = "Black"
    @staticmethod #Decorator
    def start():
        print("Car Started...")
    @staticmethod
    def stop():
        print("Car Stopped...")

class ToyotaCar(Car):
    def __init__(self, name, type):
        super().__init__(type)
        self.name = name
        self.type = type
        super().start()

car1 = ToyotaCar("Prius", "Electric")
print(car1.type)

class Person:
    name = "Anoyomous"
    def changeName1(self, name):
        self.name = name
    def changeName1(self, name):
        Person.name = name

class Person:
    name = "Anoyomous"
    def changeName1(self, name): #obj
        self.__class__.name = "Rahul"
        #self.__class_.Person

    @classmethod
    def changeName2(cls, name):
        cls.name = name

p1 = Person()
p1.changeName1("Rahul Kumar")
print(p1.name)
print(Person.name)

'''
class Student:
    @classmethod
    def college(cls):
        pass
'''

class Student:
    def __init__(self, phy, chem, math):
        self.phy = phy
        self.chem = chem
        self.math = math
        self.percentage = str((self.phy + self.chem + self.math) / 3) + "%" #percentage
    def calcPerc(self):
        self.percentage = str((self.phy + self.chem + self.math) / 3) + "%"

stu1 = Student(98, 97, 99)
print(stu1.percentage)
stu1.phy = 86
print(stu1.phy)
stu1.calcPerc()
print(stu1.percentage)