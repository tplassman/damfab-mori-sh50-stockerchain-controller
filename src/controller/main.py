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

    def run_chain(self, target_pot, loop_callback=None, reached_callback=None):
        if self.motion_running:
            return  # Prevent multiple motions
        self.motion_running = True
        timeout = self.config.timeout_seconds
        num_pots = self.config.num_pots

        def motion_loop():
            forward = 0
            reverse = 0
            active_pot = self.read_display()

            # Calculate shortest direction using modulo arithmetic
            forward_steps = (target_pot - active_pot) % num_pots
            reverse_steps = (active_pot - target_pot) % num_pots
            if forward_steps < reverse_steps:
                direction = "forward"
                forward = 1
            else:
                direction = "reverse"
                reverse = 1

            start_time = time.time()
            while self.motion_running and direction:
                print(f"Moving chain {direction} towards pot {target_pot}...")
                self.ljm.set_relay(forward=forward, reverse=reverse)
                active_pot = self.read_display()
                if loop_callback:
                    loop_callback(active_pot, direction)

                # Want to stop chain one pot before the target to avoid overshoot issues
                offset = 1 if self.config.stop_early else 0
                if (
                    (forward and (active_pot + offset) % num_pots == target_pot) # One pot before
                    or (reverse and (active_pot - offset) % num_pots == target_pot) # One pot before
                    or (active_pot == target_pot) # Direct hit check
                    or (timeout and (time.time() - start_time) > timeout) # Timeout check
                ):
                    print(f"Target pot {target_pot} reached or timeout occurred.")
                    if reached_callback:
                        reached_callback(active_pot)

                    break

                time.sleep(0.05)

            self.stop_chain()

        self.motion_thread = threading.Thread(target=motion_loop, daemon=True)
        self.motion_thread.start()

    def reverse_chain(self, loop_callback=None):
        if self.motion_running:
            return
        self.motion_running = True

        def motion_loop():
            while self.motion_running:
                print("Reversing chain...")
                self.ljm.set_relay(forward=0, reverse=1)
                active_pot = self.read_display()
                if loop_callback:
                    loop_callback(active_pot, "reverse")
                time.sleep(0.05)

        self.motion_thread = threading.Thread(target=motion_loop, daemon=True)
        self.motion_thread.start()


    def forward_chain(self, loop_callback=None):
        if self.motion_running:
            return
        self.motion_running = True

        def motion_loop():
            while self.motion_running:
                print("Moving chain forward...")
                self.ljm.set_relay(forward=1, reverse=0)
                active_pot = self.read_display()
                if loop_callback:
                    loop_callback(active_pot, "forward")
                time.sleep(0.05)

        self.motion_thread = threading.Thread(target=motion_loop, daemon=True)
        self.motion_thread.start()

    def stop_chain(self):
        self.motion_running = False
        self.ljm.set_relay(forward=0, reverse=0)