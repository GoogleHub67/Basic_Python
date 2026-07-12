tup1 = (2, 1, 3, 1)
print(type(tup1))
print(tup1[0])
print(tup1[1])
#tup[0] = 5 is not allowed because Tuples are immutable

tup2 = ()
print(tup2)
print(type(tup2))

tup3 = (1,)
print(tup3)
print(type(tup3))

tup4 = (1)
print(tup4)
print(type(tup4))

tup5 = (2.02)
print(tup5)
print(type(tup5))

tup6 = ("Python")
print(tup6)
print(type(tup6))
#Python will consider a single value as an int/float/str. For a single value, it is compulsory to put a comma to make Python consider it a tuple.

tup7 = (1, 2, 3, 4,) #Extra comma in end
print(tup7)
print(type(tup7))

tup8 = (5, 6, 7, 8, 9, 0)
print(tup8)
print(type(tup8))
#Putting a comma in the end is COMPLETELY OPTIONAL. Python will still perceive it as a tuple.

tup9 = (1, 8, 13, 14)
print(tup9[1:3])