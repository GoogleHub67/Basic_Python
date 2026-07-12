class Car:
    color = "Black"
    @staticmethod
    def start():
        print("Car Started...")
    @staticmethod
    def stop():
        print("Car Stopped...")

class ToyotaCar(Car):
    def __init__(self, name):
        self.name = name
car1 = ToyotaCar("Fortuner")
car2 = ToyotaCar("Prius")
print(car1.name)
print(car1.start())
print(car1.color)

class ToyotaCar(Car):
    def __init__(self, brand):
        self.brand = brand

class Fortuner(ToyotaCar):
    def __init__(self, type):
        self.type = type

car3 = Fortuner("Diesel")
car3.start()

class A:
    varA = "Welcome to class A"

class B:
    varB = "Welcome to class B"

class C(A, B):
    varC = "Welcome to class C"
c1 = C()
print(c1.varC)
print(c1.varB)
print(c1.varA)