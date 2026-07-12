#Abstraction
class Car:
    def __init__(self):
        self.acc = False #Accelerator
        self.brk = False #Break
        self.clutch = False
    def start(self):
        self.clutch = True
        self.acc = True
        print("Car Started...")
car1 = Car()
car1.start()

#Encapsulation