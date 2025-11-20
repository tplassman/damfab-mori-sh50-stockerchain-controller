from tkinter import Frame, Label

class Overlay:
    def __init__(self, root, message="Manual Mode Inactive"):
        self.root = root
        self.overlay = None
        self.message = message

    def is_visible(self):
        return self.overlay is not None

    def show(self):
        if self.overlay is not None:
            return
        self.overlay = Frame(self.root, bg="#888")
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay.lift()
        label = Label(
            self.overlay,
            text=self.message,
            font=("Arial", 32, "bold"),
            bg="#888",
            fg="#fff",
            padx=40,
            pady=30
        )
        label.place(relx=0.5, rely=0.5, anchor="center")
        # Block all events
        self.overlay.bind("<Button>", lambda e: "break")
        self.overlay.bind("<Key>", lambda e: "break")

    def hide(self):
        if self.overlay is not None:
            self.overlay.destroy()
            self.overlay = None