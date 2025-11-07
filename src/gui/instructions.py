from tkinter import Frame, Label, Text, X, Button, BOTTOM
from tkinter import ttk

class Instructions(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="#eee", **kwargs)
        Label(self, text="Instructions", font=("Arial", 22, "bold"), fg="#222", bg="#eee").pack(pady=(10, 0))

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=1, padx=5, pady=5)

        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook.Tab', font=('Arial', 16, 'bold'), padding=[10, 10])

        self.active_pot_tab = Frame(self.tabs, bg="#fff")
        self.target_pot_tab = Frame(self.tabs, bg="#fff")
        self.tabs.add(self.target_pot_tab, text="Target Pot")
        self.tabs.add(self.active_pot_tab, text="Active Pot")
        self.tabs.select(self.active_pot_tab)

        # --- Active Pot Instructions ---
        self.active_pot_frame = Frame(self.active_pot_tab, bg="#fff")
        self.active_pot_frame.pack(fill="both", expand=1)

        self.active_pot_text = Text(self.active_pot_frame, wrap="word", font=("Arial", 14), bg="#fff", height=18)
        self.active_pot_text.pack(side="top", fill="both", expand=1, padx=10, pady=(10, 0))
        self.active_pot_text.config(state="disabled")  # Make readonly

        # Navigation buttons for Active Pot tab (BOTTOM, fill X)
        self.active_nav_frame = Frame(self.active_pot_frame, bg="#fff")
        self.active_nav_frame.pack(side=BOTTOM, fill=X)
        self.active_up_btn = Button(self.active_nav_frame, text="▲", font=("Arial", 18), command=lambda: self.scroll_text(self.active_pot_text, -1))
        self.active_up_btn.pack(side="left", padx=0, pady=5, fill=X, expand=True)
        self.active_down_btn = Button(self.active_nav_frame, text="▼", font=("Arial", 18), command=lambda: self.scroll_text(self.active_pot_text, 1))
        self.active_down_btn.pack(side="left", padx=0, pady=5, fill=X, expand=True)

        # --- Target Pot Instructions ---
        self.target_pot_frame = Frame(self.target_pot_tab, bg="#fff")
        self.target_pot_frame.pack(fill="both", expand=1)

        self.target_pot_text = Text(self.target_pot_frame, wrap="word", font=("Arial", 14), bg="#fff", height=18)
        self.target_pot_text.pack(side="top", fill="both", expand=1, padx=10, pady=(10, 0))
        self.target_pot_text.config(state="disabled")  # Make readonly

        # Navigation buttons for Target Pot tab (BOTTOM, fill X)
        self.target_nav_frame = Frame(self.target_pot_frame, bg="#fff")
        self.target_nav_frame.pack(side=BOTTOM, fill=X)
        self.target_up_btn = Button(self.target_nav_frame, text="▲", font=("Arial", 18), command=lambda: self.scroll_text(self.target_pot_text, -1))
        self.target_up_btn.pack(side="left", padx=0, pady=5, fill=X, expand=True)
        self.target_down_btn = Button(self.target_nav_frame, text="▼", font=("Arial", 18), command=lambda: self.scroll_text(self.target_pot_text, 1))
        self.target_down_btn.pack(side="left", padx=0, pady=5, fill=X, expand=True)

        # Bind update to check button states after scrolling
        self.active_pot_text.bind("<Visibility>", lambda e: self.update_nav_buttons(self.active_pot_text, self.active_up_btn, self.active_down_btn))
        self.active_pot_text.bind("<Configure>", lambda e: self.update_nav_buttons(self.active_pot_text, self.active_up_btn, self.active_down_btn))
        self.target_pot_text.bind("<Visibility>", lambda e: self.update_nav_buttons(self.target_pot_text, self.target_up_btn, self.target_down_btn))
        self.target_pot_text.bind("<Configure>", lambda e: self.update_nav_buttons(self.target_pot_text, self.target_up_btn, self.target_down_btn))

    def scroll_text(self, text_widget, direction):
        text_widget.config(state="normal")
        text_widget.yview_scroll(direction, "units")
        text_widget.config(state="disabled")
        # Update button states after scrolling
        if text_widget == self.active_pot_text:
            self.update_nav_buttons(text_widget, self.active_up_btn, self.active_down_btn)
        else:
            self.update_nav_buttons(text_widget, self.target_up_btn, self.target_down_btn)

    def update_nav_buttons(self, text_widget, up_btn, down_btn):
        first, last = text_widget.yview()
        up_btn.config(state="normal" if first > 0 else "disabled")
        down_btn.config(state="normal" if last < 1 else "disabled")

    def load_active_pot_instructions(self, text):
        self.active_pot_text.config(state="normal")
        self.active_pot_text.delete("1.0", "end")
        self.active_pot_text.insert("end", text)
        self.active_pot_text.config(state="disabled")
        self.update_nav_buttons(self.active_pot_text, self.active_up_btn, self.active_down_btn)

    def load_target_pot_instructions(self, text):
        self.target_pot_text.config(state="normal")
        self.target_pot_text.delete("1.0", "end")
        self.target_pot_text.insert("end", text)
        self.target_pot_text.config(state="disabled")
        self.update_nav_buttons(self.target_pot_text, self.target_up_btn, self.target_down_btn)