#While Loop
#Task - Print "hello" 5 times (STEP 1 - VERY TEDIOUS AND LARGE)
print("hello")
print("hello")
print("hello")
print("hello")
print("hello")

#(STEP 2 - EASY AND SIMPLE)
count = 1
while count <= 5:
    print("hello")
    count += 1
print(count)

i_one = 1
while i_one <= 100:
    print("ApnaCollege")
    i_one += 1

i_two = 1
while i_two <= 40:
    print(i_two)
    i_two += 1

i_three = 5
while i_three >= 1:
    print("The number is", i_three)
    i_three -= 1

print("Loop Ended")
#Infinite loops are quite dangerous, recheck every loop before you run it.
#If a website has some sort of infinite loop, then there will come a point where the entire browser will crash.

#For Loop
list = [1, 2, 3, 4, 5]
for val in list:
    print(val)

veggies = ["Potato", "Brinjal", "Ladyfinger", "Cucumber"]
for val in veggies:
    print(val)

tup = (1, 2, 3, 4, 2, 8, 9)
for num in tup:
    print(num)

str = "ApnaCollege"
for char in str:
    print(char)
else:
    print("END!")

string = "ApnaCollege"
for char in string:
    if(char == "o"):
        print("Letter 'o' found!")
        break
    print(char)
#else:
print("END!") #Using else won't run it