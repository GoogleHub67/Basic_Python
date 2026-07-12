#range(start?, stop, step?), ? = Optional
#Tedious Method
seq1 = range(5)
print(seq1[0])
print(seq1[1])
print(seq1[2])
print(seq1[3])
print(seq1[4])

#Easy and Simple Method
seq2 = range(10)
for i in seq2:
    print(i)

for i in range(40): #range(stop)
    print(i)

for i in range(2, 20): #range(start, stop)
    print(i)

for i in range(2, 10, 2): #range(start, stop, step)
    print(i)

for i in range(2, 100, 2):
    print(i)

for i in range(2, 101, 2):
    print(i)

for i in range(1, 100, 2):
    print(i)