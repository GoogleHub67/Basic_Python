#STRINGS
#Creating a string
string1 = "Hello, Mehul!"
print(string1)

#Accessing Characters in Strings
#string[index]
str1 = "My name is Mehul."
print(str1[5])
#slice[n:m]
name = "My name is Mehul."
print(name[2:5])
print(name[1:4])

#Escape Characters
'''
\\ - It is used to print a backslash.
\' - It is used to print an apostrophe.
\" - It is used to print double quotataion marks.
\t - It is used to add a horizontal tab space between text.
\v - It is used to add a vertical tab space.
'''
print("It is raining.\nDon't go outside.")
str1dot1 = "It is raining."
str2 = "Don't go outside."
str3 = str1dot1 + str2
print(str3)
str3 = str1dot1 + " " + str2
print(str3)
'''
* - Repeats Strings
in - Returns True if a substring exists within a string
not in - Returns True if a substring does not exist within a string
'''
#Built-in String Methods
'''
capitalize() - Capitalizes the first letter of a string
isalpha() - Returns 'True' if the string has at least one character and all characters are letters of the alphabet
isdigit() - Returns 'True' if string has at least one character and all characters are digits
islower() - Returns 'True' if string has at least one character and all characters are in lower case
isdigit() - Returns 'True' if string has at least one character and all characters are in upper case
len(string) - Gives the length of a string
upper() - Converts lower-case letters into upper case
'''

string1dot1 = "I am learning functions in Python."
print(string1dot1.upper())
print(len(string1dot1))
#print(isdigit())