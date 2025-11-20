from tkinter import Frame, Button

class Keypad(Frame):
    def __init__(self, master, on_num_press, on_clear_press, on_del_press, **kwargs):
        super().__init__(master, **kwargs)
        self.on_num_press = on_num_press
        self.on_clear_press = on_clear_press
        self.on_del_press = on_del_press
        self.create_keypad()

    def create_keypad(self):
        buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('Clear', 3, 0), ('0', 3, 1), ('Del', 3, 2)
        ]
        for (text, row, col) in buttons:
            if text == 'Clear':
                cmd = self.on_clear_press
            elif text == 'Del':
                cmd = self.on_del_press
            else:
                cmd = lambda t=text: self.on_num_press(t)
            btn = Button(self, text=text, font=("Arial", 18), width=4, height=1, command=cmd)
            btn.grid(row=row, column=col, padx=3, pady=3)

    def disabled(self):
        for child in self.winfo_children():
            child.config(state="disabled")

    def enabled(self):
        for child in self.winfo_children():
            child.config(state="normal")