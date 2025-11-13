from tkinter import Toplevel, Frame, Label

class Overlay:
    def __init__(self, root, message="Manual Mode Inactive"):
        self.root = root
        self.overlay = None
        self.message = message

    def show(self):
        if self.overlay is not None:
            return
        self.overlay = Toplevel(self.root)
        self.overlay.overrideredirect(True)
        self.overlay.attributes('-alpha', 0.5)  # 50% opacity
        self.overlay.configure(bg="#888")
        self.overlay.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}+{self.root.winfo_x()}+{self.root.winfo_y()}")

        # Add a frame for the label with solid background and padding
        msg_frame = Frame(self.overlay, bg="#222")
        msg_frame.pack(expand=True, padx=40, pady=40)
        label = Label(
            msg_frame,
            text=self.message,
            font=("Arial", 32, "bold"),
            bg="#222",
            fg="#fff",
            padx=40,
            pady=30
        )
        label.pack(expand=True)

        self.overlay.lift()
        self.overlay.grab_set()  # Block events to main window

    def hide(self):
        if self.overlay is not None:
            self.overlay.destroy()
            self.overlay = None