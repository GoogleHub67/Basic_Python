class Student:
    def __init__(self, phy, chem, math):
        self.phy = phy
        self.chem = chem
        self.math = math
        #self.percentage = str((self.phy + self.chem + self.math) / 3) + "%" #percentage
    #def calcPerc(self):
    #    self.percentage = str((self.phy + self.chem + self.math) / 3) + "%"
    @property
    def percentage(self):
        return str((self.phy + self.chem + self.math) / 3) + "%"
stu1 = Student(98, 97, 99)
print(stu1.percentage)
stu1.phy = 86
# print(stu1.phy)
# stu1.calcPerc()
print(stu1.percentage)