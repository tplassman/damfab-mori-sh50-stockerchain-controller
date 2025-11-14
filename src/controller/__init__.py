import threading
import time

class Controller:
    def __init__(self, config, ljm):
        self.config = config
        self.ljm = ljm
        self.motion_running = False
        self.motion_thread = None

    def is_manual_control_active(self):
        return self.ljm.is_manual_control_active()

    def read_display(self):
        return self.ljm.read_display()

    def run_chain(self, target_pot, loop_callback, reached_callback):
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
                loop_callback(active_pot, direction)

                # Want to stop chain one pot before the target to avoid overshoot issues
                if (
                    (direction == "forward" and (active_pot + 1) % num_pots == target_pot) #One pot before
                    or (direction == "reverse" and (active_pot - 1) % num_pots == target_pot) #One pot before
                    or (active_pot == target_pot) #Direct hit check
                    or (timeout and (time.time() - start_time) > timeout) #Timeout check
                ):
                    reached_callback(active_pot)

                    break

                time.sleep(0.05)

            self.stop_chain()

        self.motion_thread = threading.Thread(target=motion_loop, daemon=True)
        self.motion_thread.start()

    def reverse_chain(self):
        if self.motion_running:
            return
        self.motion_running = True
        self.ljm.set_relay(forward=0, reverse=1)

    def forward_chain(self):
        if self.motion_running:
            return
        self.motion_running = True
        self.ljm.set_relay(forward=1, reverse=0)

    def stop_chain(self):
        self.motion_running = False
        self.ljm.set_relay(forward=0, reverse=0)