#Break Statement
iter = 1
while 1 <= 5:
    print(iter)
    if (iter == 3):
        break
    iter += 1

print("End of Loop!")

int_grp = (1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 36)
number = 36
iterator = 0 
while iterator < len(int_grp):
    if(int_grp[iterator] == number):
        print("Found at index", iterator)
        break
    else:
        print("Finding...")
    iterator += 1
print("End of Loop!")

#Continue Statement
i = 0
while i <= 5:
    if(i == 3): #3 won't come
        i += 1
        continue
    print(i)
    i += 1

i_alt = 0
while i_alt <= 10:
    if(i_alt % 2 == 0): #Even numbers won't come
        i_alt += 1
        continue
    print(i_alt)
    i_alt += 1

i_xtra = 0
while i_xtra <= 10:
    if(i_xtra % 2 != 0): #Odd numbers won't come
        i_xtra += 1
        continue
    print(i_xtra)
    i_xtra += 1

#Pass Statement
'''
for i in range(5):
    #empty
print("Some useful work")
This is an example of where you can use pass statements without leaving the block empty and Python showing an error.
'''
for i in range(5):
    pass

if i > 5:
    pass

print("Some useful work")