#Let's Practice Some Exercises

#Q1. Store following word meanings in a Python dictionary: 
"""
table : "a piece of furniture", "list of facts and figures"
cat : "a small animal"
"""
dict = {
    "table" : ["a piece of furniture", "list of facts and figures"],
    "cat" : "a small animal"
}
print(dict)

#Q2. You are given a list of subjects for students. Assume one classroom is required for 1 subject. How many classrooms are needed by all students?
subjects = {"Python", "Java", "C++", "Python", "JavaScript", "Java", "Python", "Java", "C++", "C"}
All_ClassRooms = len(subjects)
print(All_ClassRooms)

#Q3. Write a program to enter marks of 3 subjects from the user and store them in a dictionary. Start with an empty dictionary & add one by one. Use subject name ad key & marks as value.
marks = {}
Sub1 = int(input("Enter marks of Physics: "))
marks.update({"Physics" : Sub1})
Sub2 = int(input("Enter marks of Chemistery: "))
marks.update({"Chemistery" : Sub2})
Sub3 = int(input("Enter marks of Maths: "))
marks.update({"Maths" : Sub3})
print(marks)

#Q4. Find out a way to store 9 & 9.0 as seperate values in the set. (You can take help of built-in data types)
Num1 = int(9)
Num2 = str(9.0)
Num_set = {Num1, Num2}
print(Num_set)