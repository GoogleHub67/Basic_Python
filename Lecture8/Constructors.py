class Student:
    #Default Constructors
    def __init__(self, name, marks):
        pass
    #Parameterized Constructors
    coll = "ABC College"
    name = "Anonyomous"
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks
        print("Adding New Student in Database...")
s1 = Student("Karan", 97)
print(s1.name, s1.marks)
s2 = Student("Arjun", 88)
print(s2.name, s2.marks)
print(s1.coll)
print(s2.coll)
print(Student.coll)