import yaml

class Config:
    def __init__(self, path="config.yaml"):
        with open(path, "r") as f:
            self.data = yaml.safe_load(f)

    @property
    def dev_mode(self):
        return self.data.get("dev_mode", False)

    @property
    def stop_early(self):
        return self.data.get("stop_early", False)

    @property
    def num_pots(self):
        return self.data["num_pots"]

    @property
    def manual_control_pin(self):
        return self.data["manual_control_pin"]

    @property
    def manual_delay_seconds(self):
        return self.data.get("manual_delay_seconds", 5)

    @property
    def seven_segment_type(self):
        return self.data["seven_segment_type"]

    @property
    def segment_pins(self):
        return self.data["segment_pins"]

    @property
    def binary_pins(self):
        return self.data["binary_pins"]

    @property
    def relay_pins(self):
        return self.data["relay_pins"]

    @property
    def timeout_seconds(self):
        return self.data.get("timeout_seconds", 60)