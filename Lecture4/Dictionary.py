info = {
    "key" : "value",
    "name" : "ApnaCollege",
    "learning" : "coding",
    "age" : 35,
    "is_adult" : True,
    "marks" : 94.4,
    "Subjects" : ["Maths", "Science", "Social Studies", "Computers", "Language"],
    "Topics" : ("Dict", "Set"),
    12.99 : 45,
    64 : 56,
    True : False,
    None : "57",
    (1, 2, 3) : ["A", "B", "C"],
}

print(info)
print(type(info))
print(info["name"])
#print(info["f6"]) doesn't not work because it is not there, so error comes

games = {
    "Chess" : 1500, 
    "Roblox" : 250, 
    "Geometry Dash" : 80
}

games["Chess"] = 1100
print(games)

sub_marks = {
    "Maths" : 96,
    "Science" : 97,
    "Social Studies" : 93,
    "Computers" : 98,
    "Languages" : 90
}

sub_marks["GK"] = 95
print(sub_marks)

null_dict = {}
null_dict["Name"] = "ApnaCollege"
print(null_dict)

student = {
    "Name" : "Aarav Patel",
    "Subjects" : {
        "Physics" : 97,
        "Chemistery" : 98,
        "Maths" : 95
    }
}
#Nested Dictionary Concept
print(student["Subjects"]["Chemistery"])
student["Subjects"]["Computer"] = 97.8
print(student)