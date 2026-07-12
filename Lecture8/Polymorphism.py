print(1+2) #3
print(type[1]) #Integer
print("Apna" + "College") #Apna College, Concatenation
print(type("Apna")) #String
print([1, 2, 3] + [4, 5, 6]) #Merging
print(type([1, 2, 3])) #List

class Complex:
    def __init__(self, real, img):
        self.real = real
        self.img = img
    def showNum(self):
        print(self.real,"i +", self.img, "j")
    def __add__(self, num2):
        newReal = self.real + num2.real
        newImg = self.img + num2.img
        return Complex(newReal, newImg)
    def __sub__(self, num2):
        newReal = self.real - num2.real
        newImg = self.img - num2.img
        return Complex(newReal, newImg)

num1 = Complex(1, 3)
num1.showNum()

num2 = Complex(4, 6)
num2.showNum()

# print(num1 + num2)
num3 = num1 + num2
# print(num3)
# num3 = num1.add(num2)
# print(num3)
num3.showNum()

num4 = num1 - num2
num4.showNum()

#Others are also there, such as multiplication, division, powers, and more.