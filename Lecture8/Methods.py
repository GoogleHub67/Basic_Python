#Non Static Methods (+Using Self)
class Student1:
    coll = "ABC College"
    def __init__(self, name1, marks1):
        self.name1 = name1
        self.marks1 = marks1
    def welcome(self):
        print("Welcome Student,", self.name1)
    def get_marks(self):
        return self.marks1
s1 = Student1("Karan", 97)
s1.welcome()
print(s1.get_marks())

#Static Methods
class Student2:
    def __init__(self, name2, marks2):
        self.name2 = name2
        self.marks2 = marks2
    @staticmethod #Decorator
    def hello():
        print("Hello!")
    def get_avg(self):
        sum = 0
        for val in self.marks2:
            sum += val
        print("Hi", self.name2,"Your average score is:", sum/len(self.marks2))
s2 = Student2("Tony Stark", [99, 98, 97])
s2.get_avg()
s2.hello()


#(class) staticmethod
