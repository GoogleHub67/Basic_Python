# marks1 = 94.4
# marks2 = 87.5
# marks3 = 95.2
# marks4 = 66.4
# marks5 = 45.1
# marks6 = 12.0

marks = [94.4, 87.5, 95.2, 66.4, 45.1, 12.0]
print(marks)
print(type(marks))
print(len(marks))
print(marks[0])
print(marks[1])

student = ["Aarav", 95.4, 11, "Noida"]
print(student)

ProgR_Lang = ["Python", "JavaScript", "C++", "HTML", "CSS", "PHP", "Golang"]
ProgR_Lang[6] = "Lua"
print(ProgR_Lang)
#If you put print(ProgR_Lang[12]), it will show an error "Out of Range"

str1 = "Hello"
print(str1[0]) 
str1[0] = "y"
#Mutation not possible in Strings, but possible in Lists