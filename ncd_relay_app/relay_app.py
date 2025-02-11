import tkinter as tk
from tkinter import ttk
import serial
import RPi.GPIO as GPIO
import yaml

# Load configuration
with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Initialize serial port
ser = serial.Serial(config['serial']['port'], config['serial']['baudrate'], timeout=1)

# GPIO setup
GPIO.setmode(GPIO.BCM)
relay_pins = config['gpio']['relay_pins']
for pin in relay_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Function to toggle relay
def toggle_relay(relay):
    current_state = GPIO.input(relay_pins[relay])
    GPIO.output(relay_pins[relay], not current_state)

# GUI setup
class RelayApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NCD.io Relay Control")
        self.configure(bg='black')

        # Create buttons
        self.buttons = []
        for i in range(4):
            button = ttk.Button(self, text=f"Relay {i+1}", command=lambda i=i: toggle_relay(i))
            button.grid(row=i, column=0, padx=10, pady=10)
            self.buttons.append(button)

        # Settings Button
        settings_button = ttk.Button(self, text="Settings", command=self.open_settings)
        settings_button.grid(row=4, column=0, padx=10, pady=10)

    def open_settings(self):
        settings_window = tk.Toplevel(self)
        settings_window.title("Settings")
        settings_window.configure(bg='black')

        for i in range(4):
            label = ttk.Label(settings_window, text=f"Relay {i+1} Settings:")
            label.grid(row=i, column=0, padx=10, pady=10)
            entry = ttk.Entry(settings_window)
            entry.grid(row=i, column=1, padx=10, pady=10)

if __name__ == "__main__":
    app = RelayApp()
    app.mainloop()