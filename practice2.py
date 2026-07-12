#FUNCTIONS
#Creating a Function
def area (l, b):
    return l*b
def sum(a1, b1):
    return(a1 + b1)
def add(a2, b2):
    c = a2 + b2
    print(c)
    return
#Calling a Function
def printer(st):
    print(st)
st = "I'm in a function."
printer(st)
#Return Statement
#Example 1: To add two numbers
def add(a3, b3):
    sum = a3 + b3
    return sum
a3 = 20
b3 = 30
sum = add(a3, b3)
print(sum)
#Example 2: To find the square of a number
def square(a):
    result = a**2
    return result
result = square(14)
print(result)
#Example 3: To check whether a number is prime or not
def check_prime(n):
    if(n == 1):
        return False
    elif(n == 2):
        return True
    else:
        for x in range(2, n):
            if(n % x) == 0:
                return False
            return True
print(check_prime(20))