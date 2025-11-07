import math
from tkinter import Canvas

class Chain(Canvas):
    def __init__(self, master, num_pots=20, active_pot=1, width=300, height=300, **kwargs):
        super().__init__(master, width=width, height=height, bg="#222", highlightthickness=0, **kwargs)
        self.num_pots = num_pots
        self.width = width
        self.height = height
        self.radius = min(width, height) // 2 - 40
        self.max_render_pots = 12
        self.set_value(active_pot)

    def set_value(self, active_pot):
        self.delete("all")
        cx, cy = self.width // 2, self.height // 2

        # Calculate angle offset so active pot is at the top (north)
        angle_offset = -math.pi / 2 - (2 * math.pi * (active_pot - 1) / self.num_pots)

        # Draw large ring
        self.create_oval(cx - self.radius, cy - self.radius, cx + self.radius, cy + self.radius, outline="#888", width=8)

        # Draw tick marks for all pots
        for i in range(self.num_pots):
            angle = 2 * math.pi * i / self.num_pots + angle_offset
            tick_length = 10
            x1 = cx + (self.radius - tick_length) * math.cos(angle)
            y1 = cy + (self.radius - tick_length) * math.sin(angle)
            x2 = cx + (self.radius + tick_length) * math.cos(angle)
            y2 = cy + (self.radius + tick_length) * math.sin(angle)
            self.create_line(x1, y1, x2, y2, fill="#bbb", width=2)

        # Render only every other pot or up to max_render_pots
        step = max(1, self.num_pots // self.max_render_pots)
        for i in range(0, self.num_pots, step):
            angle = 2 * math.pi * i / self.num_pots + angle_offset
            pot_radius = 16
            x = cx + self.radius * math.cos(angle)
            y = cy + self.radius * math.sin(angle)
            is_active = (i == active_pot - 1)
            fill = "#e53935" if is_active else "#fff"
            outline = "#e53935" if is_active else "#888"
            self.create_oval(x-pot_radius, y-pot_radius, x+pot_radius, y+pot_radius, fill=fill, outline=outline, width=3)
            self.create_text(x, y, text=str(i+1), fill="#222" if not is_active else "#fff", font=("Arial", 14, "bold"))