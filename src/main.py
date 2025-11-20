import time
from tkinter import Tk
from gui import GUI
from controller import Controller
from controller.labjack import LabJackController
from controller.mock import MockController
from config_loader import Config

def check_manual_control(gui, controller, delay, poll_interval=500):
    try:
        enabled = controller.is_manual_control_active()
    except Exception:
        print("Error checking manual control status")
        enabled = False

    # When switching form auto to manual, add delay to allow the machine to ready itself
    if gui.overlay.is_visible() and enabled:
        time.sleep(delay)

    gui.set_enabled(enabled)
    gui.root.after(poll_interval, check_manual_control, gui, controller, delay, poll_interval)

if __name__ == "__main__":
    config = Config("config.yaml")

    if config.dev_mode:
        ljm = MockController(config=config, active_pot=42)
    else:
        ljm = LabJackController(config=config)

    controller = Controller(config=config, ljm=ljm)
    root = Tk()
    gui = GUI(root, controller=controller) 

    check_manual_control(gui, controller, delay=config.manual_delay_seconds)
    root.mainloop()