from controller import LabJackController

if __name__ == "__main__":
    lj = LabJackController()
    if lj.handle:
        print("Connection test passed.")
        lj.close()
    else:
        print("Connection test failed.")