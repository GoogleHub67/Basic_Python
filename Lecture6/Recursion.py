#Recursive Function
def show(n1):
    if (n1 == 0):
        return
    print(n1)
    show(n1 - 1)
show(5) #5 = n, 4 = n - 1, 3 = n - 2, 2 = n - 3, 1
print("Seperator")

def show(n2):
    if (n2 == -1):
        return
    print(n2)
    show(n2 - 1)
show(5)
print("Seperator")

def show(n3):
    if (n3 == 0):
        return
    print(n3)
    show(n3 - 1)
    print("END!")
show(3)

# def show(n4):
#     print(n4)
#     show(n4 - 1)
#     print("END!")
# show(3)
#Base Case is important in recursion because otherwise, it will become a sort-of infinite loop. But instead of running infinitely, it shows an error, unlike in a loop.

def fact(n5):
    if(n5 == 1 or n5 == 0):
        return 1
    return fact(n5-1) * n5
print(fact(2))
print(fact(4))
print(fact(5))
print(fact(6))