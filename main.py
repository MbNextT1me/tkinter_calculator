import tkinter as tk
from tkinter import ttk
from buttonsLogic import ButtonsLogic

def on_key_press(event):
    key = event.char
    if key.isdigit() or key in ['+', '-', '*', '/', '.', '(', ')']:
        buttons_logic.button_click(key)
    elif key == '=':
        buttons_logic.button_equal()
    return 'break'


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Калькулятор")

    entry_font = ('Arial', 24)
    button_font = ('Arial', 14)

    entry = ttk.Entry(window, width=20, font=entry_font, justify="right")
    entry.bind('<Key>', on_key_press)
    entry.bind('<Return>', lambda event: buttons_logic.button_equal())
    buttons_logic = ButtonsLogic(entry)
    buttons_logic.set_entry_style(entry)
    entry.grid(row=0, column=0, columnspan=4, sticky="nsew")
    entry.insert(tk.END, "0")

    entry.focus_set()

    entry.bind('<Key>', on_key_press)

    buttons = []
    button_labels = [7, 8, 9, 4, 5, 6, 1, 2, 3]

    button_grid_info =[(str(number), lambda number=number: buttons_logic.button_click(number), i // 3 + 3, i % 3) for i, number in enumerate(button_labels)]

    button_data = [
        ("0", lambda: buttons_logic.button_click(0), 6, 1),
        ("+", lambda: buttons_logic.button_click("+"), 5, 3),
        ("-", lambda: buttons_logic.button_click("-"), 4, 3),
        ("\u00D7", lambda: buttons_logic.button_click("*"), 3, 3),
        ("=", buttons_logic.button_equal, 6, 3),
        ("С", buttons_logic.button_clear, 1, 2),
        ("%", buttons_logic.button_percent, 1, 0),
        ("CE", buttons_logic.button_clean_entry, 1, 1),
        ("\u2190", buttons_logic.button_backspace_action, 1, 3),
        ("+/-", buttons_logic.button_change_sign, 6, 0),
        (".", buttons_logic.button_decimal, 6, 2),
        ("1/x", buttons_logic.button_inverse, 2, 0),
        ("x^2", buttons_logic.button_square, 2, 1),
        ("√x", buttons_logic.button_square_root_2, 2, 2),
        ("\u00F7", lambda: buttons_logic.button_click("/"), 2, 3),
    ]

    for label, command, row, column in button_grid_info + button_data:
        button = buttons_logic.create_button(window, label, command)
        button.grid(row=row, column=column, sticky="nsew")
        buttons.append(button)

    for i in range(7):
        window.grid_rowconfigure(i, weight=1)

    for i in range(4):
        window.grid_columnconfigure(i, weight=1)

    window.minsize(width=300, height=300)
    window.mainloop()
