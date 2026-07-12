#Read and ReadLine Method
f = open("demo.txt", "r")
data = f.read()
print(data)
print(type(data))
f.close()

f = open("demo.txt", "r")
data = f.read(5)
print(data)
f.close()

f = open("demo.txt", "r")
line1 = f.readline()
print(line1)
f.close()

f = open("demo.txt", "r")
data = f.read()
print(data)
line1 = f.readline()
print(line1)
line2 = f.readline()
print(line2)
f.close()
#Data can be read only once per time.

f = open("demo.txt", "r")
line1 = f.readline()
print(line1)
line2 = f.readline()
print(line2)
line3 = f.readline()
print(line3)
f.close()

#Write Method
f = open("demo.txt", "w")
f.write("I want to learn JavaScript tomorrow. 123")
f.close()
#This data just got completely overwritten.

#Append Method
f = open("demo.txt", "a")
f.write("Then I'll move to ReactJS.")
f.close()

f = open("demo.txt", "a")
f.write("\nAfter that NodeJS.")
f.close()

#If you write a file that does not exist and you try to open in W or A mode, Python will create that file for you automatically.
f = open("sample1.txt", "w")
f.close()

f = open("sample2.txt", "a")
f.close()

#Read and Write Method, But Not Truncated
f = open("demo.txt", "r+")
f.write("ABC")
print(f.read())
f.close()

#Read and Write Method, Truncated
f = open("demo.txt", "w+")
print(f.read())
f.write("ABC")
f.close()

#Append and Write Method
f = open("demo.txt", "a+")
print(f.read())
f.write("ABC")
f.close()

#Delete Method
import os
os.remove("sample2.txt")