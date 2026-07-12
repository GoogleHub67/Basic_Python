count = 1
while count < 3:

#Input x and y
    x = float(input("Enter x: "))
    y = float(input("Enter y: "))

    #Choose mode of operation
    print("Choose operation: +  -  *  /  %  **  //")
    opr = input("Operation: ")

    if opr == "+":
        result = x + y
    elif opr == "-":
        result = x - y
    elif opr == "*":
        result = x * y
    elif opr == "/":
        if y == 0:
            result = "Error: Division by zero!"
        else:
            result = x / y
    elif opr == "%":
        if y == 0:
            result = "Error: Division by zero!"
        else:
            result = x % y
    elif opr == "**":
        result = x ** y
    elif opr == "//":
        if y == 0:
            result = "Error: Division by zero!"
        else:
            result = x // y
    else:
        result = "Invalid operation!"

    print("Result:", result)

    count += 1