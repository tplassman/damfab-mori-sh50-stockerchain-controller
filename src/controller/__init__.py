import threading
import time

class Controller:
    def __init__(self, config, ljm):
        self.config = config
        self.ljm = ljm
        self.motion_running = False
        self.motion_thread = None

    def read_display(self):
        return self.ljm.read_display()

    def run_chain(self, target_pot, callback):
        if self.motion_running:
            return  # Prevent multiple motions
        self.motion_running = True
        timeout = self.config.timeout_seconds
        num_pots = self.config.num_pots

        def motion_loop():
            active_pot = self.read_display()

            # Calculate shortest direction using modulo arithmetic
            forward_steps = (target_pot - active_pot) % num_pots
            reverse_steps = (active_pot - target_pot) % num_pots
            if forward_steps < reverse_steps:
                direction = "forward"
            else:
                direction = "reverse"

            start_time = time.time()
            while self.motion_running and direction:
                forward = int(direction == "forward")
                reverse = int(direction == "reverse")
                self.ljm.set_relay(forward=forward, reverse=reverse)
                active_pot = self.read_display()
                callback(active_pot, direction)

                # Overshoot detection
                if direction == "forward" and (active_pot - target_pot) % num_pots == 0:
                    break
                if direction == "reverse" and (target_pot - active_pot) % num_pots == 0:
                    break

                # Stop if reached target pot
                if active_pot == target_pot:
                    break

                # Timeout check
                if timeout and (time.time() - start_time) > timeout:
                    break

                time.sleep(0.5)

            self.stop_chain()

        self.motion_thread = threading.Thread(target=motion_loop, daemon=True)
        self.motion_thread.start()

    def stop_chain(self):
        self.motion_running = False
        self.ljm.set_relay(forward=0, reverse=0)