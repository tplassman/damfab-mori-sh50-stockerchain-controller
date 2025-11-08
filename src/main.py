from tkinter import Tk
from gui import GUI
from controller import Controller
from controller.labjack import LabJackController
from controller.mock import MockController
from config_loader import Config

if __name__ == "__main__":
    config = Config("config.yaml")

    if config.dev_mode:
        ljm = MockController(config=config, active_pot=42)
    else:
        ljm = LabJackController(config=config)

    controller = Controller(config=config, ljm=ljm)
    root = Tk()
    gui = GUI(root, controller=controller) 
    root.mainloop()