#Let's Practice Some Exercises
#Q1. Create a new file "practice.txt" using Python. Add the following data in it:
'''
Hi everyone
we are learning File I/O
using Java.
I like programming in Java.
'''

with open("practice.txt", "w") as f:
    f.write("Hi everyone\nwe are learning File I/O\n")
    f.write("using Java.\nI like programming in Java.")

#Q2. Write a function that replaces all occurences of "Java" with "Python" in above file.
with open("practice.txt", "r") as f:
    data = f.read()
new_data = data.replace("Java", "Python")
print(new_data)
with open("practice.txt", "w") as f:
    f.write(new_data)

#Function Form
def replace_occurence():
    with open("practice.txt", "r") as f:
        data = f.read()
    new_data = data.replace("everyone", "everybody")
    print(new_data)
    with open("practice.txt", "w") as f:
        f.write(new_data)
replace_occurence()

#Q3. Search if the word "learning" exists in the file or not.
word = "learning"
with open("practice.txt", "r") as f:
    data = f.read()
    if(data.find(word) != -1):
        print("Found!")
    else:
        print("Not Found!")

#Sample
word = "Hello"
with open("practice.txt", "r") as f:
    data = f.read()
    if(data.find(word) != -1):
        print("Found!")
    else:
        print("Not Found!")

#Function Form
def check_for_word():
    word = "learning"
    with open("practice.txt", "r") as f:
        data = f.read()
        if(data.find(word) != -1):
            print("Found!")
        else:
            print("Not Found!")
check_for_word()

#Q4. Write a function to find in which line of the file does the word "learning" occur first. Print -1 if the word is not found.
def check_for_line():
    word = "learning"
    data = True
    line_num = 1
    with open("practice.txt", "r") as f:
        while data:
            data = f.readline()
            if(word in data):
                print("Found at line number", line_num)
                return
            line_num += 1
    return -1
print(check_for_line())

#Sample
def check_for_line():
    word = "programming"
    data = True
    line_num = 1
    with open("practice.txt", "r") as f:
        while data:
            data = f.readline()
            if(word in data):
                print("Found at line number", line_num)
                return
            line_num += 1
    return -1
print(check_for_line())

def check_for_line():
    word = "pyq" #Does not exist
    data = True
    line_num = 1
    with open("practice.txt", "r") as f:
        while data:
            data = f.readline()
            if(word in data):
                print("Found at line number", line_num)
                return
            line_num += 1
    return -1
print(check_for_line())

#Q5. From a file containing numbers seperated by comma, print the count of even numbers.
with open("practice.txt", "w") as f:
    f.write("1, 2, 76, 84, 90, 101")
with open("practice.txt", "r") as f:
    data = f.read()
    print(data)
    num = ""
    for i in range(len(data)):
        if(data[i] == ","):
            print(int(num))
            num = ""
        else:
            num += data[i]

#Alternate Method
count = 0
with open("practice.txt", "r") as f:
    data = f.read()
    print(data)
    nums = data.split(",")
    for val in nums:
        if(int(val) % 2 == 0):
            count += 1
print(count)