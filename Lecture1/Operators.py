#Arithmetic Operators
a = 5
b = 6
sum = a + b
print(sum)

a = 2
b = 3
difference = a - b
print(difference)

a = 4
b = 7
product = a*b
print(product)

a = 1
b = 8
quotient = a/b
print(quotient)

a = 0
b = 9
remainder = a % b
print(remainder) #remainder

a = 4.3
b = 3.5
exponent = a ** b
print(exponent) #a^b

#Relational Operators
a = 50
b = 20
print(a == b) #False
print(a != b) #True
print(a >= b) #True
print(a > b) #True
print(a <= b) #False
print(a < b) #False

#Assignment Operators
num = 10
num += 10 #10+10 => 20 
num -= 10 #10-10 => 0 
num *= 10 #10*10 => 100 
num /= 10 #10/10 => 1 
num %= 10 #10%10 => 0
num **= 10 #10^10 => 10B 
print("num : ", num)

#Logical Operators
a = 50
b = 30
print(not (a > b))
print(not False)
print(not False)

val1 = True
val2 = False
print("AND operator:", val1 and val2)
print("OR operator:", (a == b) or (a > b))