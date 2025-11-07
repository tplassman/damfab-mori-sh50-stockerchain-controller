from tkinter import Frame, Label, Button, RIGHT, X

class StatusBar(Frame):
    def __init__(self, master, on_close, **kwargs):
        super().__init__(master, bg="#333", **kwargs)
        self.pack(fill=X)
        self.connection_label = Label(self, text="LabJack: Disconnected", font=("Arial", 14), fg="#fff", bg="#333")
        self.connection_label.pack(side="left", padx=10)
        self.direction_label = Label(self, text="Direction: N/A", font=("Arial", 14), fg="#fff", bg="#333")
        self.direction_label.pack(side="left", padx=10)
        self.close_button = Button(self, text="Close", font=("Arial", 14, "bold"), bg="#e53935", fg="#fff", command=on_close)
        self.close_button.pack(side=RIGHT, padx=10)

    def update_status(self, connected, direction):
        status = "LabJack: Connected" if connected else "LabJack: Disconnected"
        self.connection_label.config(text=status)
        self.direction_label.config(text=f"Direction: {direction}")