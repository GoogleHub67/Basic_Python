#Add Method
set1 = set() #Empty Set
set1.add("Red")
set1.add("Green")
set1.add("Blue")
set1.add("Blue") #Duplicate, Ignored
set1.add(34)
set1.add((1, 4, 67, "Hi")) #Tuple
#set1.add([1, 5, 69, "Hello"]) is a list and is mutable unlike a set so it will display an error.
print(set1)
print(len(set1))

#Remove Method
set2 = {"Google", "Microsoft", "Apple"}
set2.remove("Apple")
print(set2)
#set2.remove("None") shows an error because it is not there.

#Clear Method
set3 = {"Curly", "Small", "Large", "Bar"}
print(set3)
print(len(set3))
set3.clear()
print(set3)
print(len(set3))

#Pop Method
set4 = {"Hello", "ApnaCollege", "World", "Coding", "Python"}
print(set4.pop())
print(set4)
print(set4.pop()) #Twice, but optional
print(set4)

#Union Method
set5 = {1, 2, 3}
set6 = {3, 4, 5}
print(set5.union(set6)) #{1, 2, 3, 4, 5}, Duplicates Ignored
print(set5) #No change
print(set6) #Also no change

#Intersection Method

#For Odd Number of Quantities (Excluding Duplicates)
set7 = {6, 7, 8}
set8 = {8, 9, 0}
print(set7.intersection(set8)) #{8}
print(set7)
print(set8)

#For Even Number of Quantities (Excluding Duplicates)
set9 = {12, 13, 14}
set10 = {13, 14, 15}
print(set9.intersection(set10)) #{13, 14}
print(set9)
print(set10)