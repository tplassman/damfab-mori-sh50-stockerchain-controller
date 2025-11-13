from tkinter import Tk
from gui import GUI
from controller import Controller
from controller.labjack import LabJackController
from controller.mock import MockController
from config_loader import Config

def check_manual_control(gui, controller, poll_interval=500):
    try:
        enabled = controller.is_manual_control_active()
    except Exception:
        enabled = False

    print(f"Manual control active: {enabled}")
    gui.set_enabled(enabled)
    gui.root.after(poll_interval, check_manual_control, gui, controller, poll_interval)

if __name__ == "__main__":
    config = Config("config.yaml")

    if config.dev_mode:
        ljm = MockController(config=config, active_pot=42)
    else:
        ljm = LabJackController(config=config)

    controller = Controller(config=config, ljm=ljm)
    root = Tk()
    gui = GUI(root, controller=controller) 

    check_manual_control(gui, controller)
    root.mainloop()