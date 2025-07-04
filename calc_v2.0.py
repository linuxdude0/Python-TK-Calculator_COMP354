import customtkinter as ctk
from tkinter import *
from math import *

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")  

DISPLAY_FONT = ("SF Pro Display", 28, "bold")
BUTTON_FONT = ("SF Pro Display", 16, "bold")
HISTORY_FONT = ("SF Mono", 12)
SMALL_BUTTON_FONT = ("SF Pro Display", 12, "bold")

COLORS = {
    'bg': '#1a1a1a',
    'display_bg': '#2d2d2d',
    'display_text': '#ffffff',
    'number_btn': '#404040',
    'operator_btn': '#ff9500',
    'function_btn': '#505050',
    'special_btn': '#606060',
    'history_bg': '#252525',
    'accent': '#007AFF'
}

class Calculator:
    def __init__(self):
        self.calc = ctk.CTk()
        self.calc.title("Scientific Calculator")
        self.calc.geometry("480x720")
        self.calc.resizable(False, False)
        self.calc.configure(fg_color=COLORS['bg'])
        
        # Configure grid weights
        self.calc.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.calc.grid_rowconfigure(0, weight=1)
        self.calc.grid_rowconfigure(1, weight=0)
        self.calc.grid_rowconfigure(2, weight=0)
        for i in range(3, 14):
            self.calc.grid_rowconfigure(i, weight=1)
        
        self.setup_ui()
        
    def setup_ui(self):
        # History panel
        history_frame = ctk.CTkFrame(self.calc, fg_color=COLORS['history_bg'], corner_radius=15)
        history_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=15, pady=(15, 5))
        
        history_label = ctk.CTkLabel(history_frame, text="History", font=SMALL_BUTTON_FONT, text_color="#888888")
        history_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        self.history_listbox = Listbox(
            history_frame, 
            font=HISTORY_FONT, 
            bg=COLORS['history_bg'], 
            fg="#cccccc",
            selectbackground=COLORS['accent'],
            selectforeground="white",
            borderwidth=0,
            highlightthickness=0,
            activestyle="none"
        )
        self.history_listbox.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.history_listbox.bind('<<ListboxSelect>>', self.history_onclick)
        
        # Display
        display_frame = ctk.CTkFrame(self.calc, fg_color=COLORS['display_bg'], corner_radius=15)
        display_frame.grid(row=1, column=0, columnspan=4, sticky="ew", padx=15, pady=5)
        
        self.input_box = ctk.CTkEntry(
            display_frame,
            font=DISPLAY_FONT,
            height=80,
            justify="right",
            fg_color="transparent",
            text_color=COLORS['display_text'],
            border_width=0
        )
        self.input_box.pack(fill="x", padx=20, pady=15)
        self.input_box.bind("<Return>", self.answer)
        
        # Clear history button
        clear_hist_btn = ctk.CTkButton(
            self.calc,
            text="Clear History",
            font=SMALL_BUTTON_FONT,
            height=35,
            fg_color=COLORS['special_btn'],
            hover_color="#707070",
            command=self.clr_history_listbox
        )
        clear_hist_btn.grid(row=2, column=0, columnspan=4, sticky="ew", padx=15, pady=5)
        
        # Button layout
        self.create_buttons()
        
    def create_buttons(self):
        buttons = [
            # Row 1: Advanced functions
            [
                ("√", lambda: self.input_num("sqrt("), COLORS['function_btn']),
                ("∛", lambda: self.input_num("**(1/3)"), COLORS['function_btn']),
                ("|x|", lambda: self.input_num("abs("), COLORS['function_btn']),
                ("x!", lambda: self.input_num("factorial("), COLORS['function_btn'])
            ],
            # Row 2: Trigonometric functions
            [
                ("sin⁻¹", lambda: self.input_num("asin("), COLORS['function_btn']),
                ("cos⁻¹", lambda: self.input_num("acos("), COLORS['function_btn']),
                ("tan⁻¹", lambda: self.input_num("atan("), COLORS['function_btn']),
                ("π", lambda: self.input_num("pi"), COLORS['function_btn'])
            ],
            # Row 3: Trigonometric functions
            [
                ("sin", lambda: self.input_num("sin("), COLORS['function_btn']),
                ("cos", lambda: self.input_num("cos("), COLORS['function_btn']),
                ("tan", lambda: self.input_num("tan("), COLORS['function_btn']),
                ("e", lambda: self.input_num("e"), COLORS['function_btn'])
            ],
            # Row 4: Logarithmic functions
            [
                ("log", lambda: self.input_num("log("), COLORS['function_btn']),
                ("ln", lambda: self.input_num("log("), COLORS['function_btn']),
                ("xʸ", lambda: self.input_num("**"), COLORS['function_btn']),
                ("x²", lambda: self.input_num("**2"), COLORS['function_btn'])
            ],
            # Row 5: Utility functions
            [
                ("%", lambda: self.input_num("%"), COLORS['operator_btn']),
                ("CE", lambda: self.clear_display(), COLORS['special_btn']),
                ("C", lambda: self.clear_display(), COLORS['special_btn']),
                ("⌫", lambda: self.backspace(), COLORS['special_btn'])
            ],
            # Row 6: Parentheses and division
            [
                ("(", lambda: self.input_num("("), COLORS['operator_btn']),
                (")", lambda: self.input_num(")"), COLORS['operator_btn']),
                ("1/x", lambda: self.input_num("1/"), COLORS['function_btn']),
                ("÷", lambda: self.input_num("/"), COLORS['operator_btn'])
            ],
            # Row 7: Numbers and multiplication
            [
                ("7", lambda: self.input_num("7"), COLORS['number_btn']),
                ("8", lambda: self.input_num("8"), COLORS['number_btn']),
                ("9", lambda: self.input_num("9"), COLORS['number_btn']),
                ("×", lambda: self.input_num("*"), COLORS['operator_btn'])
            ],
            # Row 8: Numbers and subtraction
            [
                ("4", lambda: self.input_num("4"), COLORS['number_btn']),
                ("5", lambda: self.input_num("5"), COLORS['number_btn']),
                ("6", lambda: self.input_num("6"), COLORS['number_btn']),
                ("−", lambda: self.input_num("-"), COLORS['operator_btn'])
            ],
            # Row 9: Numbers and addition
            [
                ("1", lambda: self.input_num("1"), COLORS['number_btn']),
                ("2", lambda: self.input_num("2"), COLORS['number_btn']),
                ("3", lambda: self.input_num("3"), COLORS['number_btn']),
                ("+", lambda: self.input_num("+"), COLORS['operator_btn'])
            ],
            # Row 10: Zero, decimal, and equals
            [
                ("±", lambda: self.toggle_sign(), COLORS['special_btn']),
                ("0", lambda: self.input_num("0"), COLORS['number_btn']),
                (".", lambda: self.input_num("."), COLORS['number_btn']),
                ("=", lambda: self.answer(), COLORS['accent'])
            ]
        ]
        
        start_row = 3
        for row_idx, row in enumerate(buttons):
            for col_idx, (text, command, color) in enumerate(row):
                # Calculate padding
                # Outer edges get larger padding, inner buttons get small uniform padding
                pad_left = 15 if col_idx == 0 else 2
                pad_right = 15 if col_idx == len(row) - 1 else 2
                pad_top = 5 if row_idx == 0 else 2
                pad_bottom = 5 if row_idx == len(buttons) - 1 else 2

                btn = ctk.CTkButton(
                    self.calc,
                    text=text,
                    font=BUTTON_FONT,
                    height=50,
                    fg_color=color,
                    hover_color=self.get_hover_color(color),
                    corner_radius=4,
                    command=command
                )
                btn.grid(
                    row=row_idx + start_row, 
                    column=col_idx, 
                    sticky="nsew", 
                    padx=(pad_left, pad_right),
                    pady=(pad_top, pad_bottom)
                )
    
    def get_hover_color(self, base_color):
        """Generate hover color based on base color"""
        hover_colors = {
            COLORS['number_btn']: '#505050',
            COLORS['operator_btn']: '#ffb84d',
            COLORS['function_btn']: '#606060',
            COLORS['special_btn']: '#707070',
            COLORS['accent']: '#0056b3'
        }
        return hover_colors.get(base_color, '#505050')
    
    def add_to_history(self, result):
        self.history_listbox.insert(0, result)
        self.history_listbox.yview(0)
        
        # Limit history to 50 items
        if self.history_listbox.size() > 50:
            self.history_listbox.delete(50, END)
    
    def history_onclick(self, e):
        curr_selection = self.history_listbox.curselection()
        if curr_selection:
            val = self.history_listbox.get(curr_selection[0])
            if "=" in val:
                result = val.split("=")[1].strip()
                self.input_box.delete(0, END)
                self.input_box.insert(END, result)
            self.history_listbox.selection_clear(0, END)
    
    def clr_history_listbox(self):
        self.history_listbox.delete(0, END)
    
    def answer(self, event=None):
        expression = self.input_box.get().strip()
        if not expression:
            return
            
        try:
            # Handle special cases
            if expression.startswith("ln("):
                expression = expression.replace("ln(", "log(", 1)
            
            result = eval(expression)
            
            # Format result for display
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            self.input_box.delete(0, END)
            self.input_box.insert(END, str(result))
            self.add_to_history(f"{expression} = {result}")
            
        except Exception as e:
            self.input_box.delete(0, END)
            self.input_box.insert(END, "Error")
    
    def input_num(self, num):
        current = self.input_box.get()
        
        # Clear if showing error
        if current == "Error":
            current = ""
        
        new_value = current + str(num)
        self.input_box.delete(0, END)
        self.input_box.insert(END, new_value)
    
    def clear_display(self):
        self.input_box.delete(0, END)
    
    def backspace(self):
        current = self.input_box.get()
        if current and current != "Error":
            self.input_box.delete(0, END)
            self.input_box.insert(0, current[:-1])
    
    def toggle_sign(self):
        current = self.input_box.get()
        if current and current != "Error":
            if current.startswith("-"):
                self.input_box.delete(0, END)
                self.input_box.insert(0, current[1:])
            else:
                self.input_box.delete(0, END)
                self.input_box.insert(0, "-" + current)
    
    def run(self):
        self.calc.mainloop()

if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()