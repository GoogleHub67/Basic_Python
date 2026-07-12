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
