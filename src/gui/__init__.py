import os

from tkinter import Frame, Label, Button, PanedWindow, BOTH, HORIZONTAL
from .seven_segment import SevenSegmentDisplay
from .keypad import Keypad
from .instructions import Instructions
from .status_bar import StatusBar
from .chain import Chain

class GUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.target_pot_value = 0

        active_pot = controller.read_display()
        if (active_pot is None):
            print("Warning: Could not read active pot from LabJack. Defaulting to 0.")
            active_pot = 0

        root.title("Stocker Chain Controller")
        root.attributes('-fullscreen', True) 

        # Top: Status Bar
        self.status_bar = StatusBar(root, on_close=self.close_app)
        self.status_bar.pack(fill="x")
        self.paned = PanedWindow(root, orient=HORIZONTAL)
        self.paned.pack(fill=BOTH, expand=1)

        # Left: Active Pot Display
        self.left_frame = Frame(self.paned, bg="#222")
        self.paned.add(self.left_frame, minsize=200)
        Label(self.left_frame, text="Active Pot", font=("Arial", 18, "bold"), fg="#fff", bg="#222").pack(pady=10)
        self.active_pot_display = SevenSegmentDisplay(self.left_frame, digits=2, value=active_pot, scale=1.5)
        self.active_pot_display.pack(pady=20)
        self.stocker_chain = Chain(self.left_frame, self.controller.config.num_pots, active_pot)
        self.stocker_chain.pack(pady=10)

        # Center: Keypad, Target Pot, Run/Stop
        self.center_frame = Frame(self.paned, bg="#f5f5f5")
        self.paned.add(self.center_frame, minsize=400)
        Label(self.center_frame, text="Target Pot", font=("Arial", 16, "bold"), fg="#222", bg="#f5f5f5").pack(pady=5)
        self.target_pot_display = SevenSegmentDisplay(self.center_frame, digits=2, value=0, scale=1.0)
        self.target_pot_display.pack(pady=5)
        self.keypad = Keypad(self.center_frame, on_num_press=self.num_press, on_clear_press=self.clear_press, on_del_press=self.del_press, bg="#f5f5f5")
        self.keypad.pack(pady=10)
        self.button_frame = Frame(self.center_frame, bg="#f5f5f5")
        self.button_frame.pack(pady=10)
        self.run_button = Button(self.button_frame, text="Run", font=("Arial", 24, "bold"), bg="#43a047", fg="#fff", width=8, height=2, command=self.run_chain, state="disabled")
        self.run_button.grid(row=0, column=0, padx=10)
        self.stop_button = Button(self.button_frame, text="Stop", font=("Arial", 24, "bold"), bg="#e53935", fg="#fff", width=8, height=2, command=self.stop_chain, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=10)

        # Right: Instructions Tabs
        self.instructions = Instructions(self.paned)
        self.paned.add(self.instructions, minsize=300)

        if active_pot != 0:
            self.update_active_pot(active_pot, "None")

    def num_press(self, key):
        current = str(self.target_pot_value)
        if len(current) < 2:  # Limit to two digits
            current += key
            self.target_pot_value = int(current)
            self.update_target_pot(self.target_pot_value)
        self.validate_target_pot()

    def clear_press(self):
        self.target_pot_value = 0
        self.update_target_pot(self.target_pot_value)
        self.validate_target_pot()

    def del_press(self):
        current = str(self.target_pot_value)
        current = current[:-1] if current else ""
        self.target_pot_value = int(current) if current else 0
        self.update_target_pot(self.target_pot_value)
        self.validate_target_pot()

    def validate_target_pot(self):
        max_pot = self.controller.config.num_pots
        valid = 1 <= self.target_pot_value <= max_pot
        self.run_button.config(state="normal" if valid else "disabled")

    def set_chain_running(self, running):
        if running:
            self.run_button.config(state="disabled")
            self.stop_button.config(state="normal")
        else:
            self.run_button.config(state="normal")
            self.stop_button.config(state="disabled")

    def update_active_pot(self, value, direction):
        self.status_bar.update_status(self.controller.ljm.is_connected(), direction.title())
        self.active_pot_display.set_value(value)
        self.stocker_chain.set_value(value)
        if value == self.target_pot_value:
            self.status_bar.update_status(self.controller.ljm.is_connected(), "None")
            self.target_pot_value = 0
            self.update_target_pot(self.target_pot_value)
            self.load_instructions(value, target=False)
            self.instructions.tabs.select(self.instructions.active_pot_tab)
            self.set_chain_running(False)

    def update_target_pot(self, value):
        self.target_pot_display.set_value(value)
        self.load_instructions(value, target=True)
        self.instructions.tabs.select(self.instructions.target_pot_tab)
        self.validate_target_pot()

    def load_instructions(self, pot_number, target=True):
        pot_str = f"{pot_number:02d}"
        filename = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),  # project root
            "instructions",
            f"pot{pot_str}.txt"
        )
        try:
            with open(filename, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            text = f"No instructions found for Pot {pot_str}."
        if target:
            self.instructions.load_target_pot_instructions(text)
        else:
            self.instructions.load_active_pot_instructions(text)

    def run_chain(self):
        self.controller.run_chain(self.target_pot_value, self.update_active_pot)
        self.set_chain_running(True)

    def stop_chain(self):
        self.controller.stop_chain()
        self.set_chain_running(False)

    def close_app(self):
        self.root.destroy()