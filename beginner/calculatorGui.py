########################################
#Author: Nicholas Dubs
#Date: 20/10/24
#FileName: calculatorGui
#Description: simple calculator with a gui
########################################
import tkinter as tk
import tkinter.messagebox
from tkinter.constants import SUNKEN

window = tk.Tk()
window.title('Calculator')
frame = tk.Frame(master=window, bg="skyblue", padx=10)
frame.pack()
entry = tk.Entry(master=frame, relief=SUNKEN, borderwidth=3, width=30)
entry.grid(row=0,column=0,columnspan=3,ipadx=2, ipady=2)

def myclick(number):
    entry.insert(tk.END, number)

def equal():
    try:
        y = str(eval(entry.get()))
        entry.delete(0,tk.END)
        entry.insert(0,y)
    except:
        tkinter.messagebox.showinfo("Error","Syntax Error")
    
def clear():
    entry.delete(0, tk.END)

def round_result():
    """
    Round the current result to the nearest whole number.
    """
    try:
        current_value = float(entry.get())  # Get the current value in the entry
        rounded_value = round(current_value)  # Round the value
        entry.delete(0, tk.END)
        entry.insert(0, str(rounded_value))  # Insert the rounded value back into the entry
    except ValueError:
        tkinter.messagebox.showinfo("Error", "No valid number to round")

button_1 = tk.Button(master=frame, text='1', padx=15, pady=5, width=3, command=lambda: myclick(1))
button_2 = tk.Button(master=frame, text='2', padx=15, pady=5, width=3, command=lambda: myclick(2))
button_3 = tk.Button(master=frame, text='3', padx=15, pady=5, width=3, command=lambda: myclick(3))
button_4 = tk.Button(master=frame, text='4', padx=15, pady=5, width=3, command=lambda: myclick(4))
button_5 = tk.Button(master=frame, text='5', padx=15, pady=5, width=3, command=lambda: myclick(5))
button_6 = tk.Button(master=frame, text='6', padx=15, pady=5, width=3, command=lambda: myclick(6))
button_7 = tk.Button(master=frame, text='7', padx=15, pady=5, width=3, command=lambda: myclick(7))
button_8 = tk.Button(master=frame, text='8', padx=15, pady=5, width=3, command=lambda: myclick(8))
button_9 = tk.Button(master=frame, text='9', padx=15, pady=5, width=3, command=lambda: myclick(9))
button_0 = tk.Button(master=frame, text='0', padx=15, pady=5, width=3, command=lambda: myclick(0))

button_add = tk.Button(master=frame, text='+', padx=15, pady=5, width=3, command=lambda: myclick('+'))
button_sub = tk.Button(master=frame, text='-', padx=15, pady=5, width=3, command=lambda: myclick('-'))
button_mult = tk.Button(master=frame, text='*', padx=15, pady=5, width=3, command=lambda: myclick('*'))
button_div = tk.Button(master=frame, text='/', padx=15, pady=5, width=3, command=lambda: myclick('/'))
button_sqr = tk.Button(master=frame, text='^', padx=15, pady=5, width=3, command=lambda: myclick('**'))
button_root = tk.Button(master=frame, text='sqrt', padx=15, pady=5, width=3, command=lambda: myclick('**(1/2)'))
button_clear = tk.Button(master=frame, text='clear', padx=15, pady=5, width=12, command=clear)
button_equal = tk.Button(master=frame, text='=', padx=15, pady=5, width=12, command=equal)
button_round = tk.Button(master=frame, text='Round', padx=15, pady=5, width=3, command=round_result)

# Grid layout for the buttons
button_1.grid(row=1, column=0, pady=2)
button_2.grid(row=1, column=1, pady=2)
button_3.grid(row=1, column=2, pady=2)

button_4.grid(row=2, column=0, pady=2)
button_5.grid(row=2, column=1, pady=2)
button_6.grid(row=2, column=2, pady=2)

button_7.grid(row=3, column=0, pady=2)
button_8.grid(row=3, column=1, pady=2)
button_9.grid(row=3, column=2, pady=2)

button_0.grid(row=4, column=1, pady=2)

button_add.grid(row=5, column=0, pady=2)
button_sub.grid(row=5, column=1, pady=2)
button_mult.grid(row=5, column=2, pady=2)

button_div.grid(row=6, column=0, pady=2)
button_sqr.grid(row=4, column=0, pady=2)
button_root.grid(row=4, column=2, pady=2)

button_clear.grid(row=6, column=1, columnspan=2, pady=2)
button_equal.grid(row=7, column=0, columnspan=2, pady=2)
button_round.grid(row=7, column=2, columnspan=1, pady=2)

window.mainloop()
    
