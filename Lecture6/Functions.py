'''
def func_name(param1, param2...):
    #some work
    return val
func_name(arg1, arg2...) #function call
'''

#We should use functions in place of redundant code.
#Bulky, Complex Situation
a1 = 5
b1 = 10
sum1 = a1 + b1
print(sum)

#MORE LINES OF CODE

a2 = 2
b2 = 10
sum2 = a2 + b2
print(sum)

#MORE LINES OF CODE

a3 = 12
b3 = 17
sum3 = a3 + b3
print(sum)

#Simple Situation

def calc_sum(a4, b4):
    sum4 = a4 + b4
    print(sum4)
    return sum4

calc_sum(5, 10)

#MORE LINES OF CODE

calc_sum(2, 10)

#MORE LINES OF CODE

calc_sum(12, 17)

#Function Definition
def calc_sum(a5, b5): #Parameters
    return a5 + b5
sum5 = calc_sum(1, 2) #3
print(sum5)
sum6 = calc_sum(178, 2221) #2399 #Function Call; Arguements
print(sum6)

def print_Hello():
    print("hello")

print_Hello()
print_Hello()
print_Hello()
print_Hello()
print_Hello()

output = print_Hello() 
print(output) #None

def calc_Avg(num1, num2, num3):
    num_list = [num1, num2, num3]
    Avg = (num1 + num2 + num3)/ len(num_list)
    print(Avg)
    return Avg
calc_Avg(1, 2, 3)
calc_Avg(98, 97, 95)
calc_Avg(-5, 2, 3)

#Built-In Functions

#Print Function
#print() is technically a function which we are learning since Lecture 1. 
'''
def print(
    *values: object,
    sep: str | None = " ",
    end: str | None = "\n",
    file: SupportsWrite[str] | None = None,
    flush: Literal[False] = False
) -> None
'''
print("ApnaCollege", "ShradhaKhapra") #Seperator (sep, check line 79) = ""
print("ApnaCollege","ShradhaKhapra") 
#Even without putting a spacebar, it added it accordingly. (HINT: Check Line 79)
print("ApnaCollege")
print("ShradhaKhapra") #End = "\n" (Check Line 80)
print("ApnaCollege", end = " ") #Sep = " "
print("ShradhaKhapra") #End = "\n"
print("ApnaCollege", end = " Hello ") 
print("ShradhaKhapra")

#Length Function
'''
len()
(function) def len(
    obj: Sized,
    /
) -> int
'''
print(len("Hi"))
print(len([4, 5, 6, 7, "Hi", ("Hello", "Length", "ApnaCollege")]))

#Type Function
#(class) type
print(type("Hi"))
print(type(56))
print(type(True))
print(type(None))
print(type(5.65))

#Range Function
'''
class range(
    stop: SupportsIndex,
    /
): ...

class range(
    start: SupportsIndex,
    stop: SupportsIndex,
    step: SupportsIndex = 1,
    /
): ...
'''
for int in range(5):
    print(int)
for el in range(32, 1024, 64):
    print(el)

#User Defined Functions
#They are functions created by ourselves, like a custom function.