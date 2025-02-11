# NCD.io Relay Control App

This application allows you to control NCD.io relays using a graphical user interface (GUI) with a dark theme. The app includes settings for networking, GPIO, serial, and GUI configurations.

## Features
- Control relays using buttons
- Dark theme GUI
- Separate settings page for button configurations
- Networking, GPIO, and serial configurations

## Requirements
- Python 3.x
- Tkinter
- pyserial
- RPi.GPIO
- PyYAML

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/ncd_relay_app.git
    cd ncd_relay_app
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python relay_app.py
    ```

## Configuration
Edit the `config/config.yaml` file to set the serial port, baud rate, and GPIO relay pins.

## License
This project is licensed under the MIT License.