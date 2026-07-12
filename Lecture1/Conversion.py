#Type Conversion
a1 = 2
b1 = 4.25
sum = a1 + b1 #2.00 + 4.25 => 6.25
print(sum) 

#Python auto-promotes integers to floats in mixed operations for precision.

#Type Casting
a2 = "2" #String type
a3 = int("2") #String type in integer, will convert to integer.
b2 = 4.25

print(type(a2)) 
print(type(a3)) 

sum = a3 + b2 #2.00 + 4.25 => 6.25
print(sum)

#Python requires manual conversion of strings to int/float for arithmetic operations.
a4 = float('Aarav1.0')
a5 = float('1ABC2.8')
a6 = int('H4H5')
a7 = int('2XYZ9.21')

a8 = 3.14
a8 = str(a8)

print(type(a8))

a9= float('Aarav')
print(a9) 
#Int/float conversion needs digits only; chars fail.
