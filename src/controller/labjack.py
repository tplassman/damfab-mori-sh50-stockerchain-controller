from labjack import ljm
from .decoder import SevenSegmentDecoder

class LabJackController:
    def __init__(self, config):
        self.config = config
        self.decoder = SevenSegmentDecoder(config.seven_segment_type)
        try:
            self.handle = ljm.openS("T4", "ANY", "ANY")
        except Exception as e:
            print(f"LabJack connection error: {e}")
            self.handle = None
        self.motion_running = False

    def is_connected(self):
        return self.handle is not None

    def is_manual_control_active(self):
        if not self.handle:
            print("LabJack not connected; cannot read manual control status.")
            return False

        return bool(ljm.eReadName(self.handle, self.config.manual_control_pin))

    def read_display(self):
        segs1 = self._read_segments(self.config.binary_pins['digit1'])
        segs2 = self._read_segments(self.config.binary_pins['digit2'])
        digit1 = self.decoder.decodeFourBitBinary(segs1)
        digit2 = self.decoder.decodeFourBitBinary(segs2)
        if digit1 is not None and digit2 is not None:
            return digit1 * 10 + digit2
        return None

    def set_relay(self, forward=False, reverse=False):
        if self.handle:
            ljm.eWriteName(self.handle, self.config.relay_pins["forward"], int(forward) * 5.0)
            ljm.eWriteName(self.handle, self.config.relay_pins["reverse"], int(reverse) * 5.0)

    def _read_segments(self, segment_pins):
        if not self.handle:
            return [0]*len(segment_pins) # Return all segments off
        pin_names = list(segment_pins.values())
        return ljm.eReadNames(self.handle, len(pin_names), pin_names)
