# #Let's Practice Some Exercises

# #Q1. Print numbers from 1 to 100.
# num1 = 1
# while num1 <= 100:
#     print(num1)
#     num1 += 1

# #Q2. Print numbers from 100 to 1.
# num2 = 100
# while num2 >= 1:
#     print(num2)
#     num2 -= 1

# #Q3. Print the multiplication table of a number n.
# num3 = int(input("Enter a number: "))
# looping_num = 1
# while looping_num <= 10:
#     print(looping_num * num3)
#     looping_num += 1

# #Q4. Print the elements of the following list using a loop: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# nums = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# idx1 = 0
# while idx1 < len(nums):
#     print(nums[idx1])
#     idx1 += 1

# #Traversing
# heroes = ["IronMan", "Thor", "BatMan", "SuperMan"]
# idx2 = 0
# while idx2 < len(heroes):
#     print(heroes[idx2])
#     idx2 += 1

# # idx = 0
# # while idx < len(nums):
# #     print(nums[idx]) #nums[0], nums[1], nums [2]... nums[len(nums) - 1]
# #     idx += 1

# #Q5. Search for a number x in this tuple using loop: (1, 4, 9, 16, 25, 36, 49, 64, 81, 100)
# int_grp1 = (1, 4, 9, 16, 25, 36, 49, 64, 81, 100)
# x1 = 36
# i1 = 0 #Initialization
# while i1 < len(int_grp1):
#     if(int_grp1[i1] == x1):
#         print("Found at index", i1)
#     i1 += 1

# #Sample(s)
# int_grp2 = (1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 36)
# x2 = 36
# i2 = 0 
# while i2 < len(int_grp2):
#     if(int_grp2[i2] == x2):
#         print("The number is at index", i2)
#     else:
#         print("Finding...")
#     i2 += 1

# int_grp3 = (1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 36)
# x3 = 67
# i3 = 0 
# while i3 < len(int_grp3):
#     if(int_grp3[i3] == x3):
#         print("The number is at index", i3)
#     else:
#         print("Finding continued...")
#     i3 += 1

# #Q6. (using for) Print the elements of the following list using a loop: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# list = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# for el in list:
#     print(el)

# #Q7. (using for) Search for a number x in this tuple using loop: (1, 4, 9, 16, 25, 36, 49, 64, 81, 100)
# tuple = (1, 4, 9, 16, 25, 36, 49, 64, 81, 100)
# x4 = 64
# num4 = 0 #Index

# for el in tuple: #Element
#     if(el == x4):
#         print("The number", x4, "has been found at index number", num4)
#         num4 += 1
# #This process is called Linear Search

# #Q8. (using for & range()) Print numbers from 1 to 100.
# for i in range(1, 101, 1):
#     print(i)

# #Q9. (using for & range()) Print numbers from 100 to 1.
# for i in range(100, 0, -1):
#     print(i)

# #Q10. (using for & range()) Print the multiplication table of a number.
# num5 = int(input("Enter a number: "))
# for i in range(1, 11):
#     print(num5 * i)

# #Q11. Write a program to find the sum of first 'n' numbers. (using while)
# #While
# num6 = int(input("Enter the stopping number: "))
# sum1 = 0
# initializer1 = 1
# while initializer1 <= num6:
#     sum1 += initializer1
#     initializer1 += 1
# print("Total Sum =", sum1)

# #For
# num7 = int(input("Enter the stopping number: "))
# sum2 = 0
# for i in range(1, num7 + 1):
#     sum2 += i
# print("Total Sum =", sum2)

#Q12. Write a program to find the factorial of first 'n' numbers. (using for)
num8 = int(input("Enter a number: "))
factorial = 1
initializer2 = 1
while initializer2 <= num8:
    factorial *= initializer2
    initializer2 += 1
print("Factorial = ", factorial)