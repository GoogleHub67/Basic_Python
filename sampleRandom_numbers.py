import random

my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

# To ensure non-repeated elements, first convert the list to a set
# to remove duplicates, then convert it back to a list.
unique_list = list(set(my_list))

# Select one random element from the unique list
random_element = random.sample(unique_list, 1)[0]

print(f"The original list: {my_list}")
print(f"The unique elements in the list: {unique_list}")
print(f"A non-repeated random element from the list: {random_element}")

import random

items = ["apple", "banana", "cherry", "date", "apple"]

random.shuffle(items)  #shuffles in place
for x in items:
    print(x)