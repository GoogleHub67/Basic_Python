#Checking if someone is eligible to vote
age = 95
if(age >= 18):
    if(age >= 80):
        print("Cannot vote")
        print("Cannot drive")
    else:
        print("Can vote")
        print("Can drive")
else:
    print("Cannot vote")
    print("Cannot drive")

#Traffic Light Problem
light = "Green"
if(light == "Red"):
    print("Stop!")
elif(light == "Green"):
    print("Go!")
elif(light == "Yellow"):
    print("Look!") or print("Wait!")
else:
    print("Light is broken")

print("End of code!")

#Finding if a number is greater than another number
num = 5
if(num > 2):
    print("Greater than 2")
if(num > 3):
    print("Greater than 3")

#Marks
marks = input("Enter the student's marks: ")

if(marks >= 90):
    grade = "A"
elif(marks >= 80 and marks < 90):
    grade = "B"
elif(marks >= 70 and marks <80):
    grade = "C"
else:
    grade = "D"

print("Grade of the student ->", grade)