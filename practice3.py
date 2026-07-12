#LOOPS
#The Input() Function
var = input("Prompt String")
name = input("What is your name?")
print("My name is: ", name)
num1 = int(input("Enter the radius of the circle:\n"))
area = 3.14 * num1 * num1
print("Area of the circle is", area)
#Example 1: To check whether the number entered by the user is even or not
num2 = int(input("Enter any number of your choice:"))
if(num2 % 2) == 0:
    print("The number is even.")
else:
    print("The number is odd.")

#Looping Statements
#While Loop
counter1 = 1
while counter1 <= 5:
    counter1 = counter1 + 1
    print("Hello")
#Example 2: To display all the natural numbers from 1 to 10
counter2 = 0
while counter2 < 10:
    counter2 = counter2 + 1
    print(counter2)
#Example 3: To print the sum of the digits entered by a user
num3 = int(input("Enter a number:"))
snum = 0
while num3 > 0:
    rem = num3 % 10
    snum = snum + rem
    num = int(num / 10)
    print("The sum of the digits is", snum)

#For Loop
#for var in sequence:
#    statement(s)
numbers = [1, 2, 3, 4, 5]
for i in numbers:
    print(i)
for x in range(10, 20):
    print(x)
names = ["Rashmi", "Rohan", "Samara"]
for i in range(names):
    print(i)
for x in range(10, 20, 2):
    print(x)
#Example 4: To print the first ten numbers in the reverse order
for i in range(10, 0, -1):
    print(i)
#Example 5: To print the multiplication table of a number entered by a user
num = int(input("Enter the number for which you want to print the table: "))
for i in range(1, 11):
    print(num, "x", i, "=", num * i)

#Break Statement
#if condition:
#    break
for x in range(5):
    if(x == 2):
        break
    print(x)
print("The program ends here.")

#Continue Statement
#if condition:
#    continue
for i in range(5):
    if(i == 2):
        continue
    print(i)