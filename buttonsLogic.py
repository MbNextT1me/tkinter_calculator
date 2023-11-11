import tkinter as tk
from tkinter import ttk
import math
import re

class ButtonsLogic:
    def __init__(self, entry):
        self.entry = entry
        self.entry_font_size = 24
        self.button_font_size = 14

    def set_entry_style(self, entry):
        style = ttk.Style()
        style.configure("TEntry", padding=(5, 5))
        entry.config(style="TEntry")
        entry.bind("<Configure>", lambda event, e=entry: self.adjust_entry_font_size(event, e))
        entry['validatecommand'] = (entry.register(self.validate_entry), '%P')
        entry['validate'] = 'key'

    def validate_entry(self, new_text):
        allowed_chars = set('0123456789+-*/.()%=')
        if new_text == '' or new_text == '-' or new_text[0] == '.':
            return True
        return all(char in allowed_chars for char in new_text)

    def set_button_style(self, button):
        style = ttk.Style()
        style.configure("TButton", padding=(2, 2), relief="raised", borderwidth=2, font=('Arial', self.button_font_size))
        button.config(style="TButton")

    def create_button(self, parent, text, command=None, width=5):
        button = ttk.Button(parent, text=text, command=command, width=width)
        self.set_button_style(button)
        button.bind("<Configure>", lambda event, b=button: self.adjust_button_font_size(event, b))
        return button

    def button_click(self, number):
        current = self.entry.get()
        if current == "0" and str(number).isdigit() and len(current) == 1:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(number))
        elif len(current) > 2 and current[-2] in ['+', '*', '/', '-'] and current[-1] == "0":
            self.entry.delete(len(current) - 1, tk.END)
            self.entry.insert(tk.END, str(number))
        else:
            self.entry.insert(tk.END, str(number))
        self.entry.focus_set()

    def button_equal(self):
        current = self.entry.get()
        if current and current[-1] in ['+', '-', '*', '/']:
            current = current[:-1]

        try:
            result = eval(current)
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, result)
        except:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Ошибка")
        self.entry.focus_set() 

    def button_clear(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, "0")

    def button_percent(self):
        current = self.entry.get()
        try:
            parts = re.split(r'([-+*/])', current)

            if len(parts) == 1:  
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "0")
            elif len(parts) == 3:  
                first_number = float(parts[0])
                operator = parts[1]
                second_number = float(parts[2])
                if operator in {'+', '-'}:
                    result = first_number + (first_number * (second_number / 100))
                elif operator in {'*', '/'}:
                    result = first_number * (second_number * 0.01)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
        except ValueError:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Ошибка: Неверный формат числа")

    def button_clean_entry(self):
        current = self.entry.get()
        if current:
            last_operator_index = max(current.rfind('+'), current.rfind('-'), current.rfind('*'), current.rfind('%'))
            if last_operator_index != -1:
                self.entry.delete(last_operator_index + 1, tk.END)
            else:
                self.entry.delete(0, tk.END)

    def button_backspace_action(self):
        current = self.entry.get()
        if current:
            current = current[:-1]
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, current)

    def button_change_sign(self):
        current = self.entry.get()
        if current:
            parts = re.split(r'([-+*/])', current)

            last_number = None
            for part in reversed(parts):
                if part and part[0].isdigit():
                    last_number = part
                    break

            if last_number:
                updated_number = str(-float(last_number)) if last_number[0] != '-' else last_number[1:]
                updated_input = current.rsplit(last_number, 1)[0] + updated_number
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, updated_input)

    def button_decimal(self):
        current = self.entry.get()[:-1]
        if not current or not current[-1].isdigit() and current[-1] != '.':
            self.entry.insert(tk.END, '.')

    def button_inverse(self):
        current = self.entry.get()
        try:
            parts = re.split(r'([-+*/])', current)

            last_number = None
            for part in reversed(parts):
                if part and part[0].isdigit():
                    last_number = part
                    break

            if last_number and float(last_number) != 0:
                result = 1 / float(last_number)
                updated_input = current.rsplit(last_number, 1)[0] + str(result)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, updated_input)
            else:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Ошибка: Деление на ноль")
        except ValueError:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Ошибка: Неверный формат числа")

    def button_square(self):
        current = self.entry.get()
        try:
            parts = re.split(r'([-+*/])', current)

            last_number = None
            for part in reversed(parts):
                if part and part[0].isdigit():
                    last_number = part
                    break

            if last_number:
                squared_number = str(float(last_number) ** 2)
                updated_input = current.rsplit(last_number, 1)[0] + squared_number
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, updated_input)
        except ValueError:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Ошибка: Неверный формат числа")

    def button_square_root_2(self):
        current = self.entry.get()
        try:
            parts = re.split(r'([-+*/])', current)
            last_number = None
            for part in reversed(parts):
                if part and part[0].isdigit():
                    last_number = part
                    break

            if last_number:
                result = math.sqrt(float(last_number))
                updated_input = current.rsplit(last_number, 1)[0] + str(result)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, updated_input)
            else:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Ошибка: Нет числа для извлечения корня")
        except ValueError:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Ошибка: Неверный формат числа")

    def adjust_entry_font_size(self, event, entry):
        new_width = event.width
        new_height = event.height
        new_font_size = max(10, int(min(new_width / 15, new_height / 2)))
        if new_font_size > 46:
            new_font_size = 46
        if new_font_size != self.entry_font_size:
            self.entry_font_size = new_font_size
            new_entry_font = ('Arial', self.entry_font_size)
            self.entry.config(font=new_entry_font)

    def adjust_button_font_size(self, event, button):
        new_width = event.width
        new_height = event.height
        new_font_size = max(10, int(min(new_width / 15, new_height / 2)))
        if new_font_size > 40:
            new_font_size = 40
        if new_font_size < 14:
            new_font_size = 14
        if new_font_size != self.button_font_size:
            self.button_font_size = new_font_size
            self.set_button_style(button)