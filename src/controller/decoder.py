class SevenSegmentDecoder:
    # Segment map for common cathode digits 0-9 (a-g)
    SEGMENT_MAP = {
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

    def __init__(self, display_type="common_cathode"):
        self.display_type = display_type

    def decodeDisplay(self, segments):
        # For common anode, invert the signals
        if self.display_type == "common_anode":
            segments = [0 if s else 1 for s in segments]
        for digit, pattern in self.SEGMENT_MAP.items():
            if segments == pattern:
                return digit
        return None

    def decodeFourBitBinary(self, segments):
        # Assumes segments represent a 4-bit binary number (A, B, C, D)
        if len(segments) < 4:
            return None
        value = 0
        for i in range(4):
            if segments[i]:
                value += (1 << (3 - i))
        return value