class Student:
    def __init__(self, name):
        self.name = name
s1 = Student("Shradha")
del s1
#print(s1) shows an error because we deleted it.

s2 = Student("Michael")
print(s2)
del s2

s3 = Student("Kevin")
print(s3.name)
del s3.name