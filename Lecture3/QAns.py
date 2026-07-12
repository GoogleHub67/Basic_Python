#Let's Practice Some Exercises

#Q1. Write a program to ask the user to enter names of their 3 favourite movies and store them in a list.
Movie1 = input("Enter your first favourite movie:")
Movie2 = input("Enter your second favourite movie:")
Movie3 = input("Enter your third favourite movie:")
Movies = [Movie1, Movie2, Movie3]
print(Movies)
#Did not use append method

#Q2. Write a program to check if a list contains a palindrome of elements. (Hint: use copy() method)
list1 = [1, 2, 1]
list2 = [1, 2, 3]
copy_list1 = list1.copy()
copy_list1.reverse()
if(copy_list1 == list1):
    print("Palindrome")
else:
    print("Not a Palindrome")

#Q3.
#A. Write a program to count the number of students with the "A" grade in the following tuple: ["C", "D", "A", "A", "B", "B", "A"]
grade = ["C", "D", "A", "A", "B", "B", "A"]
print(grade.count("A"))

#B. Store the above values in a list and sort them from "A" to "D".
grade.sort()
print(grade)