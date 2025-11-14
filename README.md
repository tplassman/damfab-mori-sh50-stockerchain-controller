# Mori SH-50 Pot Controller

This is a touchscreen-based industrial pot controller for the Mori SH-50, using a LabJack T4 for hardware I/O.  
The application is built with Python and Tkinter, and is designed for easy operation and maintainability.

---

## Features

- Touchscreen UI with keypad and chain visualization
- Pot instructions loaded from `instructions/potXX.txt` files
- Manual and automatic (run-to-target) chain control
- LabJack T4 hardware integration (with mock mode for development)
- Global overlay disables UI when manual mode is inactive
- Modern Python project structure with [uv](https://github.com/astral-sh/uv) for package management

---

## Project Structure

```
src/
  main.py                # Application entry point
  config_loader.py       # Loads YAML config
  controller/
    main.py              # Main controller logic
    labjack.py           # LabJack hardware interface
    mock.py              # Mock controller for dev/testing
    decoder.py           # Seven-segment display decoder
  gui/
    main.py              # Main GUI class
    chain.py             # Chain visualization widget
    instructions.py      # Instructions pane widget
    keypad.py            # Numeric keypad widget
    overlay.py           # Overlay for global UI disable
    seven_segment.py     # Seven-segment display widget
    status_bar.py        # Status bar widget
instructions/
  pot01.txt, ...         # Per-pot instruction files
config.yaml              # Main configuration file
```

---

## Setup & Installation

### 1. Install [uv](https://github.com/astral-sh/uv) (if not already installed)

```sh
pip install uv
```

### 2. Install dependencies

From the project root (where `pyproject.toml` is located):

```sh
uv pip install
```

### 3. Configuration

Edit `config.yaml` to set the number of pots, LabJack pin assignments, and other options.

### 4. Running the Application

```sh
cd src
python main.py
```

---

## Usage

- Use the on-screen keypad to select a target pot.
- Press **Run** to move the chain to the target pot.
- Use **Forward** and **Reverse** for manual movement.
- The UI will gray out when manual mode is inactive (based on the configured control pin).
- Instructions for each pot are loaded from `instructions/potXX.txt`.

---

## Development & Testing

- To run in development mode (with mock hardware), set `dev_mode: true` in `config.yaml`.
- Place test instruction files in the `instructions/` directory (e.g., `pot25.txt`).

---

## License

MIT License

---

## Notes

- For LabJack hardware, install the appropriate drivers and ensure the device is connected.