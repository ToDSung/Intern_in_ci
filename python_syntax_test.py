def one():
    return 1
def two():
    return 2

#函式能被當作參數傳入

def sum(a,b):
    return a+b

print(sum(one(),two()))

# 函式能夠被賦值給變數
a = one()
b = two()

print(sum(a,b))        

def three():
    return one()+two()

print(three())