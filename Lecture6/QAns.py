#Let's Practice Some Exercises

#Q1. Write a function to print the length of a list. (list is the parameter)
cities = ["Delhi", "Shanghai", "Bangkok", "Tokyo", "Paris", "New York", "London"]
def print_len(list):
    print(len(list))
print_len(cities)

#Q2. Write a function to print the elements of a list in a singale line. (list is the parameter)
games = ["Call of Duty", "Geometry Dash", "Roblox", "FreeFire", "MineCraft", "Fortnite", "Grand Theft Auto V", "PlayerUnknown Battlegrounds"]
print(games[0], end= " ")
print(games[1])
def print_list(list):
    for item in list:
        print(item, end= " ")
print_list(games)
print()

#Q3. Write a function to find the factorial of n. (n is the parameter)
num1 = int(input("Enter a number: "))
def cal_fact(num1):
    fact = 1
    for i in range(1, num1 + 1):
        fact *= i
    return fact
print(cal_fact(num1))


#Q4. Write a function to convert United States Dollars (USD) to Indian Rupee (INR).
def converter(usd_val):
    inr_val = usd_val * 90
    print(usd_val, "USD =", inr_val, "INR")
converter(1)
converter(100)
converter(73)

#Homework Problem
#Q5. Write a function which will input a number and output a string "ODD" and "EVEN" depending on the number.
num2 = int(input("Enter a number: "))
def num_indicator(num2):
    if num2 % 2 == 0:
        return "EVEN"
    else:
        return "ODD"
print(num_indicator(num2))

#Q6. Write a recursive function to calculate the sum of forst 'n' natural numbers.
num3 = int(input("Enter a number: "))
def calc_sum(num3):
    if(num3 == 0):
        return 0
    return calc_sum(num3 - 1) + num3
print(calc_sum(num3))

#Q7. Write a recursive function to print all elements in a list. (HINT: Use list and index as parameters.)
def print_list(list, idx = 0):
    if(idx == len(list)):
        return
    print(list[idx])
    print_list(list, idx + 1)
social_media = ["YouTube", "TikTok", "X", "FaceBook", "Instagram", "WhatsApp", "Reddit", "SnapChat"]
print_list(social_media)