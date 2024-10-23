########################################
#Author: Nicholas Dubs
#Date: 20/10/24
#FileName: calculator.py
#Description: Basic Calulator in Python(No GUI)
########################################
import modules
from modules import menu, get_int
def add(x, y):
    return x + y
def sub(x, y):
    return x - y
def mult(x, y):
    return x*y
def div(x, y):
    return x/y
def exp(x, y):
    return x**y
def root(x, y):
    return float(x)**(1/float(y))


options = ['add', 'subtract','multiply', 'divide', 'exponent', 'root', 'exit2']
while True:
    num1 = get_int("Input 1st integer ")
    num2 = get_int("Input 2nd integer ")


    answer = menu(options)

    if answer == 0:
        print(add(num1,num2))
    elif answer == 1:
        print(sub(num1, num2))
    elif answer ==2:
        print(mult(num1,num2))
    elif answer == 3:
        print(div(num1, num2))
    elif answer == 4:
        print(exp(num1,num2))
    elif answer == 5:
        print(print(root(num1,num2)))
    elif answer==6:
        print('exiting calculator...')
        break