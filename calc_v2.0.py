import customtkinter as ctk
from tkinter import *
from math import *

def add_to_history(result) -> None:
    history_listbox.insert(0, result)
    history_listbox.yview(0)

def history_onclick(e: Event) -> None:
    currSelectionIndexes = history_listbox.curselection()
    if currSelectionIndexes:
        val = history_listbox.get(currSelectionIndexes[0])
        val = val.split("=")[1]
        input_box.insert(END, val)
        history_listbox.selection_clear(0, END)

def clr_history_listbox():
    history_listbox.delete(0, END)

def answer(event=None):
    expression = str(input_box.get())
    eval_expression = expression.replace('÷', '/').replace('×', '*').replace('^', '**').replace('²', '**2')

    try:
        evaluate = eval(eval_expression)
        input_box.delete(0, END)
        input_box.insert(END, evaluate)
        add_to_history(f"{expression}={evaluate}")
    except (TypeError, SyntaxError, NameError, ZeroDivisionError):
        input_box.delete(0, END)
        input_box.insert(END, "Error")
    except:
        input_box.delete(0, END)
        input_box.insert(END, "Error")

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

def key_press(event):
    key = event.char
    keysym = event.keysym

    if key in "0123456789.+-()^%":
        input_num(key)
    elif key == '*':
        input_num('×')
    elif key == '/':
        input_num('÷')
    elif keysym == "Return" or key == "=":
        answer()
    elif keysym == "BackSpace":
        backspace()
    elif keysym.lower() == "c" or keysym == "Escape":
        clear_display()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
FONT = "Consolas"
FONT_SIZE = 18
COLOR_OP = '#ff6b35'
COLOR_NORMAL = '#2d3748'
COLOR_ACCENT = '#48bb78'
COLOR_ENTRY_BG = '#1a202c'
COLOR_HISTORY_BG = '#2d3748'

calc = ctk.CTk()
calc.title("Scientific Calculator")
calc.configure(fg_color='#1a1a1a')

start_row = 0

history_frame = ctk.CTkFrame(calc, fg_color=COLOR_HISTORY_BG)
history_frame.grid_columnconfigure(0, weight=1)
history_frame.grid_columnconfigure(1, weight=0)

history_label = ctk.CTkLabel(history_frame,
                             text="History",
                             text_color='white',
                             font=(FONT, FONT_SIZE, 'bold'))
history_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

history_listbox = Listbox(history_frame, 
                         font=(FONT, FONT_SIZE),
                         bg=COLOR_ENTRY_BG,
                         fg='white',
                         selectbackground=COLOR_ACCENT,
                         selectforeground='black',
                         relief='flat',
                         highlightthickness=0)
history_listbox.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
history_frame.grid_rowconfigure(1, weight=1)
history_frame.grid(row=start_row, column=0, columnspan=4, sticky="nsew")

start_row+=1
calc.grid_rowconfigure(start_row, weight=1)
calc.grid_columnconfigure(0, weight=1)

input_box = ctk.CTkEntry(calc, 
                        font=(FONT, FONT_SIZE), 
                        width=300, 
                        height=45,
                        fg_color=COLOR_ENTRY_BG,
                        text_color='white',
                        border_color=COLOR_ACCENT,
                        border_width=2)
input_box.grid(row=start_row, column=0, columnspan=4, sticky='NSEW')

start_row+=1
calc.grid_rowconfigure(start_row, weight=1)
calc.grid_columnconfigure(0, weight=1)

clear_button = ctk.CTkButton(history_frame,
                            text="Clear",
                            command=lambda: clr_history_listbox(),
                            font=(FONT, 14),
                            width=60,
                            height=28,
                            fg_color=COLOR_OP,
                            hover_color='#e53e3e',
                            text_color='white')
clear_button.grid(row=0, column=1, sticky="e", padx=10, pady=5)
start_row+=1

input_box.bind("<Return>", answer)

history_listbox.bind('<<ListboxSelect>>', history_onclick)
calc.bind("<Key>", key_press)

advanced_buttons = [
    [
        ("sqrt", lambda: input_num("sqrt("), COLOR_ACCENT),
        ("cbrt", lambda: input_num("**(1/3)"), COLOR_ACCENT),
        ("|x|", lambda: input_num("abs("), COLOR_ACCENT),
    ],
    [
        ("arcsin", lambda: input_num("asin("), COLOR_ACCENT),
        ("arccos", lambda: input_num("acos("), COLOR_ACCENT),
        ("arctan", lambda: input_num("atan("), COLOR_ACCENT),
        ("!", lambda: input_num("factorial("), COLOR_ACCENT),
    ],
    [
        ("sin", lambda: input_num("sin("), COLOR_ACCENT),
        ("cos", lambda: input_num("cos("), COLOR_ACCENT),
        ("tan", lambda: input_num("tan("), COLOR_ACCENT),
        ("pi", lambda: input_num("pi"), COLOR_ACCENT),
    ],
    [
        ("log", lambda: input_num("log("), COLOR_ACCENT),
        ("ln", lambda: input_num("ln("), COLOR_ACCENT),
        ("^", lambda: input_num("^"), COLOR_OP),
        ("e", lambda: input_num("e"), COLOR_ACCENT),
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
        ("𝑥²", lambda: input_num("²"), COLOR_NORMAL),
        (")", lambda: input_num(")"), COLOR_NORMAL),
        ("÷", lambda: input_num("÷"), COLOR_OP),
    ],
    [
        ("7", lambda: input_num("7"), COLOR_NORMAL),
        ("8", lambda: input_num("8"), COLOR_NORMAL),
        ("9", lambda: input_num("9"), COLOR_NORMAL),
        ("×", lambda: input_num("×"), COLOR_OP),
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
                          corner_radius=10,
                          fg_color=buttons[row][col][2],
                          hover_color='#4a5568',
                          text_color='white',
                          border_width=1,
                          border_color='#4a5568'
                          ).grid(row=row, column=col, sticky="NEWS", padx=2, pady=2)

calc.mainloop()
