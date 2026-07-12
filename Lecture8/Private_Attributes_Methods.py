class Account:
    def __init__(self, acc_num, acc_pass):
        self.acc_num = acc_num
        self.acc_pass = acc_pass

acc1 = Account("12345", "abcde")
print(acc1.acc_num)
print(acc1.acc_pass)

class Account:
    def __init__(self, acc_num, acc_pass):
        self.acc_num = acc_num
        self.__acc_pass = acc_pass
    def reset_pass(self):
        print(self.__acc_pass)

acc2 = Account("12345", "abcde")
print(acc2.acc_num)
print(acc2.reset_pass())
#print(acc2.__acc_pass) Shows error

class Account:
    def __init__(self, acc_num, acc_pass):
        self.acc_num = acc_num
        self.__acc_pass = acc_pass

class Person:
    __name = "Anoyomous"

p1 = Person()
#print(p1.__name) Shows eroor because __ makes it private

class Person:
    name = "Anoyomous"
p2 = Person()
print(p2.name)

class Person:
    __name = "Anoyomous"
    def __hello(self, name):
        print("Hello person!")
    def welcome(self):
        self.__hello(self.__name)
p3 = Person()
#print(p3.__hello()) shows error
print(p3.welcome())