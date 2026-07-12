#Append Method
list1 = [2, 1, 3]
list1.append(4)
print(list1)

#Sort Method
#Ascending
list2 = [8, 5, 6, 4]
list2.sort()
print(list2)

list3 = [7, 19, 80, 42, -11.8]
list3.sort()
print(list3)

list4 = [23, 56, 43]
list4.append(-4.02)
list4.sort()
print(list4)

#Descending
list5 = [15.6, 65.15, 15.678, 15.56, 15.06]
list5.sort(reverse = True)
print(list5)

list6 = ["banana", "litchi", "apple", "mango"]
list6.sort(reverse = True)
print(list6)

list7 = ["A", "a", "B", "b"]
list7.sort(reverse = True)
print(list7)

list8 = ["Hi", "Hello"]
#print(list8.append(4))
list8.sort(reverse = True)
print(list8)
#Proof that we cannot sort strings and integers in the same list

list9 = ['A', 'I', 'M', 'I', 'M']
list9.sort(reverse = True)
print(list9)

#Reverse Method
list10 = ['PY', 'JS', 'JAVA', 'C++', 'C#']
list10.reverse()
print(list10)

#Insert Method
list11 = [4, 8, 13]
list11.insert(8, 16) #print((Specific_List).insert(idx, el))
print(list11)

#Remove Method
list12 = ['Append', 'Sort', 'Reverse', 'Insert', 'Remove', 'Pop']
list12.remove('Pop')
print(list12)

#Pop Method
list13 = [2, 1, 3, 1]
list13.pop(2)
print(list13)