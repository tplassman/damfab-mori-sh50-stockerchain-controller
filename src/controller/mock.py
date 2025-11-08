import time

class MockController:
    def __init__(self, config, active_pot):
        self.config = config
        self.active_pot = active_pot

    def read_display(self):
        return self.active_pot

    def set_relay(self, forward=False, reverse=False):
        num_pots = self.config.num_pots
        if not forward and not reverse:
            return 

        if forward:
            self.active_pot = (self.active_pot + 1) % num_pots
        elif reverse:
            self.active_pot = (self.active_pot - 1) % num_pots

        if self.active_pot == 0:
            self.active_pot = num_pots

        time.sleep(0.5)