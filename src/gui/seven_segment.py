from tkinter import Canvas

class SevenSegmentDisplay(Canvas):
    def __init__(self, master, digits=2, value=0, scale=1.0, **kwargs):
        super().__init__(master, width=int(80*digits*scale), height=int(120*scale), bg="#222", highlightthickness=0, **kwargs)
        self.digits = digits
        self.scale = scale
        self.value = value
        self._draw_display()

    def set_value(self, value):
        self.value = value
        self._draw_display()

    def _draw_digit(self, position, digit):
        seg_coords = [
            (20, 10, 60, 20),   # a
            (60, 20, 70, 60),   # b
            (60, 70, 70, 110),  # c
            (20, 100, 60, 110), # d
            (10, 70, 20, 110),  # e
            (10, 20, 20, 60),   # f
            (20, 55, 60, 65),   # g
        ]
        segment_map = {
            0: [1,1,1,1,1,1,0],
            1: [0,1,1,0,0,0,0],
            2: [1,1,0,1,1,0,1],
            3: [1,1,1,1,0,0,1],
            4: [0,1,1,0,0,1,1],
            5: [1,0,1,1,0,1,1],
            6: [1,0,1,1,1,1,1],
            7: [1,1,1,0,0,0,0],
            8: [1,1,1,1,1,1,1],
            9: [1,1,1,1,0,1,1],
        }
        offset_x = int(position * 80 * self.scale)
        for idx, on in enumerate(segment_map[digit]):
            color = "#e53935" if on else "#222"
            x1, y1, x2, y2 = [int(c*self.scale) for c in seg_coords[idx]]
            self.create_rectangle(x1+offset_x, y1, x2+offset_x, y2, fill=color, outline=color)

    def _draw_display(self):
        self.delete("all")
        for i in range(self.digits):
            digit = int(str(self.value).zfill(self.digits)[i])
            self._draw_digit(i, digit)
