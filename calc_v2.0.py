import customtkinter as ctk
from tkinter import *
from math import *

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")  
FONT = "Consolas"
FONT_SIZE = 15
COLOR_OP = '#ff9500'
COLOR_NORMAL = 'blue'

calc = ctk.CTk()
calc.title("Scientific Calculator")

start_row = 0

history_frame = ctk.CTkFrame(calc)
history_lablel = ctk.CTkLabel(history_frame, text="History").pack(anchor="w")
calc.grid_rowconfigure(start_row, weight=1)
calc.grid_columnconfigure(0, weight=1)

history_listbox = Listbox(history_frame, font=(FONT, FONT_SIZE))
history_listbox.pack(fill="both", expand=True, padx=10, pady=10)
history_frame.grid(row=start_row, column=0, columnspan=4, sticky="nsew")

start_row+=1
calc.grid_rowconfigure(start_row, weight=1)
calc.grid_columnconfigure(0, weight=1)

input_box = ctk.CTkEntry(calc, font=(FONT, FONT_SIZE), width=300, height=45)
input_box.grid(row=start_row, column=0, columnspan=4, sticky='NSEW')

start_row+=1
calc.grid_rowconfigure(start_row, weight=1)
calc.grid_columnconfigure(0, weight=1)

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

clear_button = ctk.CTkButton(calc, text="Clear History", command=lambda: clr_history_listbox(), font=(FONT, FONT_SIZE), width=300, height=45).grid(row=start_row, column=0, columnspan=4, sticky='NSEW')
start_row+=1

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

advanced_buttons = [
    [
        ("sqrt", lambda: input_num("sqrt("), COLOR_NORMAL),
        ("cbrt", lambda: input_num("**(1/3)"), COLOR_NORMAL),
        ("|x|", lambda: input_num("abs("), COLOR_NORMAL),
        # ("Clr Hist", lambda: clr_history_listbox(), COLOR_NORMAL)
    ],
    [
        ("arcsin", lambda: input_num("asin("), COLOR_NORMAL),
        ("arccos", lambda: input_num("acos("), COLOR_NORMAL),
        ("arctan", lambda: input_num("atan("), COLOR_NORMAL),
        ("!", lambda: input_num("factorial("), COLOR_NORMAL),
    ],
    [
        ("sin", lambda: input_num("sin("), COLOR_NORMAL),
        ("cos", lambda: input_num("cos("), COLOR_NORMAL),
        ("tan", lambda: input_num("tan("), COLOR_NORMAL),
        ("pi", lambda: input_num("pi"), COLOR_NORMAL),
    ],
    [
        ("log", lambda: input_num("log("), COLOR_NORMAL),
        ("ln", lambda: input_num("ln("), COLOR_NORMAL),
        ("^", lambda: input_num("**"), COLOR_OP),
        ("e", lambda: input_num("e"), COLOR_NORMAL),
    ],
]

normal_buttons = [
    [
        ("%", lambda: input_num("%"), COLOR_NORMAL),
        ("CE", lambda: clear_display(), COLOR_OP),
        ("C", lambda: clear_display(), COLOR_OP),
        ("⌫", lambda: backspace(), COLOR_OP),
    ],
    [
        ("(", lambda: input_num("("), COLOR_NORMAL),
        ("𝑥²", lambda: input_num("**2"), COLOR_NORMAL),
        (")", lambda: input_num(")"), COLOR_NORMAL),
        ("÷", lambda: input_num("/"), COLOR_OP),
    ],
    [
        ("7", lambda: input_num("7"), COLOR_NORMAL),
        ("8", lambda: input_num("8"), COLOR_NORMAL),
        ("9", lambda: input_num("9"), COLOR_NORMAL),
        ("×", lambda: input_num("*"), COLOR_OP),
    ],
    [
        ("4", lambda: input_num("4"), COLOR_NORMAL),
        ("5", lambda: input_num("5"), COLOR_NORMAL),
        ("6", lambda: input_num("6"), COLOR_NORMAL),
        ("-", lambda: input_num("-"), COLOR_OP),
    ],
    [
        ("1", lambda: input_num("1"), COLOR_NORMAL),
        ("2", lambda: input_num("2"), COLOR_NORMAL),
        ("3", lambda: input_num("3"), COLOR_NORMAL),
        ("+", lambda: input_num("+"), COLOR_OP),
    ],
    [
        ("+/-", lambda: input_num("-"), COLOR_NORMAL),
        ("0", lambda: input_num("0"), COLOR_NORMAL),
        (".", lambda: input_num("."), COLOR_NORMAL),
        ("=", lambda: answer(), COLOR_OP),
    ],
]

all_buttons = [
    advanced_buttons,
    normal_buttons,
]

for buttons in all_buttons:
    frame = ctk.CTkFrame(calc)
    frame.grid(row=start_row, column=0, columnspan=4, sticky="NEWS")
    start_row+=1
    for row in range(len(buttons)):
        frame.grid_rowconfigure(row, weight=1)
        for col in range(len(buttons[row])):
            frame.grid_columnconfigure(col, weight=1)
            ctk.CTkButton(frame,
                          text=buttons[row][col][0],
                          font=(FONT, FONT_SIZE),
                          command=buttons[row][col][1],
                          corner_radius=100,
                          fg_color=buttons[row][col][2]
                          ).grid(row=row, column=col, sticky="NEWS")

calc.mainloop()
