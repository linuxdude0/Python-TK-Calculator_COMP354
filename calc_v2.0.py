import customtkinter as ctk
from tkinter import *
from math import *

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")  
FONT = "Consolas"
FONT_SIZE = 15


calc = ctk.CTk()
calc.title("CALCULATOR")

input_box = ctk.CTkEntry(calc, font=(FONT, FONT_SIZE), width=300, height=45)
input_box.grid(row=1, column=0, columnspan=4, sticky='NSEW')

history_listbox = Listbox(calc, font=(FONT, FONT_SIZE))
history_listbox.grid(row=0, column=0, columnspan=4, sticky="nsew")

start_row = 2

# inserts in the listbox, scrolls to last inserted
def add_to_history(result) -> None:
    history_listbox.insert(0, result)
    history_listbox.yview(0)

def history_onclick(e: Event) -> None:
    currSelectionIndexes = history_listbox.curselection()
    if currSelectionIndexes:
        val = history_listbox.get(currSelectionIndexes[0])
        val = val.split("=")[1]
        # input_box.delete(0, END)
        input_box.insert(END, val)
        history_listbox.selection_clear(0, END)

def clr_history_listbox():
    history_listbox.delete(0, END)

def answer(event=None):
    ans = str(input_box.get())
    try:
        evaluate = eval(ans)
        input_box.delete(0, END)
        input_box.insert(END, evaluate)
        add_to_history(f"{ans}={evaluate}")
    except TypeError:
        input_box.delete(0, END)
        input_box.insert(END, "Error")
    except:
        input_box.delete(0, END)
        input_box.insert(END, "Error")

input_box.bind("<Return>", answer)

def input_num(num):
    dv = str(input_box.get())
    num = dv + str(num)
    input_box.delete(0, END)
    input_box.insert(END, num)

def clear_display():
    input_box.delete(0, END)

def backspace():
    bs = input_box.get()
    input_box.delete(0, END)
    input_box.insert(0, bs[0:-1])

history_listbox.bind('<<ListboxSelect>>', history_onclick)

buttons = [
    [
        ("sqrt", lambda: input_num("sqrt(")),
        ("cbrt", lambda: input_num("**(1/3)")),
        ("|x|", lambda: input_num("abs(")),
        ("Clr Hist", lambda: clr_history_listbox())
    ],
    [
        ("arcsin", lambda: input_num("asin(")),
        ("arccos", lambda: input_num("acos(")),
        ("arctan", lambda: input_num("atan(")),
        ("!", lambda: input_num("factorial(")),
    ],
    [
        ("sin", lambda: input_num("sin(")),
        ("cos", lambda: input_num("cos(")),
        ("tan", lambda: input_num("tan(")),
        ("pi", lambda: input_num("pi")),
    ],
    [
        ("log", lambda: input_num("log(")),
        ("ln", lambda: input_num("ln(")),
        ("^", lambda: input_num("**")),
        ("e", lambda: input_num("e")),
    ],
    [
        ("%", lambda: input_num("%")),
        ("CE", lambda: clear_display()),
        ("C", lambda: clear_display()),
        ("⌫", lambda: backspace()),
    ],
    [
        ("(", lambda: input_num("(")),
        ("𝑥²", lambda: input_num("**2")),
        (")", lambda: input_num(")")),
        ("÷", lambda: input_num("/")),
    ],
    [
        ("7", lambda: input_num("7")),
        ("8", lambda: input_num("8")),
        ("9", lambda: input_num("9")),
        ("×", lambda: input_num("*")),
    ],
    [
        ("4", lambda: input_num("4")),
        ("5", lambda: input_num("5")),
        ("6", lambda: input_num("6")),
        ("-", lambda: input_num("-")),
    ],
    [
        ("1", lambda: input_num("1")),
        ("2", lambda: input_num("2")),
        ("3", lambda: input_num("3")),
        ("+", lambda: input_num("+")),
    ],
    [
        ("+/-", lambda: input_num("-")),
        ("0", lambda: input_num("0")),
        (".", lambda: input_num(".")),
        ("=", lambda: answer()),
    ],
]

for row in range(len(buttons)):
    calc.grid_rowconfigure(row+start_row, weight=1)
    for col in range(len(buttons[row])):
        calc.grid_columnconfigure(col, weight=1)
        ctk.CTkButton(calc,
                      text=buttons[row][col][0],
                      font=(FONT, FONT_SIZE),
                      command=buttons[row][col][1]
                      ).grid(row=row+start_row, column=col, sticky="NEWS")

calc.mainloop()
