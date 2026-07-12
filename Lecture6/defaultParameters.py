'''
def cal_prod(a, b):
    print(a * b)
    return a * b
cal_prod()
'''
#The code you see above, if you try to run it, it will throw an error that two arguements are required. But there is a way that we can run that code without putting aruguements—by putting default parameter values.

def cal_prod(a = 1, b = 1):
    print(a * b)
    return a * b
cal_prod()

def cal_prod(c = 4, d = 2):
    print(c * d)
    return c * d
cal_prod()

def cal_prod(e, f = 2):
    print(e * f)
    return e * f
cal_prod(1)
#Non default arguement follows default arguement, so you can't do the opposite.
def cal_prod(h, g = 2):
    print(g * h)
    return g * h
cal_prod(1)