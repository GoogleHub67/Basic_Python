#Let's Practice Some Exercises

#Q1. Write a program to input user's first name & print its length.
name = input("Enter your name: ")
print("Length of your name is", len(name))

#Q2. Write a program to find tprint(he occurence of '$' in a String.
str1 = "$!@#*%^&$!"
print(str1.count("$"))

#Q3. Write a program to check if a number entered by the user is odd or even.
num = int(input("Enter a number:"))
remN = num % 2
if(remN == 0):
    print("Your number is even")
elif(remN == 1):
    print("Your number is odd ")
else:
    print("Invalid Number!")

#Q4. Write a program to find the greatest of 3 numbers entered by the user.
num1 = float(input("Enter your first floating number: "))
num2 = float(input("Enter your second floating number: "))
num3 = float(input("Enter your third floating number: "))
if(num1 > num2) and (num1 > num3):
    print(num1, "is the greatest number.")
elif(num2 > num1) and (num2 > num3):
    print(num2, "is the greatest number.")
elif(num3 > num1) and (num3 > num2):
    print(num3, "is the greatest number.")
elif(num1 == num2) or (num1 == num3) or (num2 == num3):
    print("Some of the numbers in the list are equal.")
else:
    print("Invalid number.")

#Q5. Write a program to check if a number is a multiple of 7 or not.
number = int(input("Enter a number: "))
if ((number % 7) == 0):
    print("This number is divisible by 7.")
elif ((number % 7) != 0):
    print("This number is not divisible by 7.")
else:
    print("Invalid number!")

#Homework Problem
#Q6. Write a program to find the greatest of 4 numbers entered by the user.
a = float(input("Enter your first floating number: "))
b = float(input("Enter your second floating number: "))
c = float(input("Enter your third floating number: "))
d = float(input("Enter your fourth floating number: "))
if(a > b) and (a > c) and (a > d):
    print(a, "is the greatest number.")
elif(b > a) and (b > c) and (b > d):
    print(b, "is the greatest number.")
elif(c > a) and (c > b) and (c > d):
    print(c, "is the greatest number.")
elif(d > a) and (d > b) and (d > d):
    print(d, "is the greatest number.")
elif(a == b) or (a == c) or (a == d) or (b == c) or (b == d) or (c == d):
    print("Some of the numbers in the list are equal.")
else:
    print("Invalid number.")