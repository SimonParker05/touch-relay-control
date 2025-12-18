# touch-relay-control

Control for NCD.io ProXR relays via network, serial, or GPIO

## Overview

This repository contains software for controlling NCD ProXR relay controllers in various configurations:

- **ProXR Firmware** (`proxr_firmware/`) - Arduino firmware for controlling 11 banks of 8 relays using AD1 dry contact input over USB
- **Python Relay App** (`ncd_relay_app/`) - GUI application for relay control via network, serial, or GPIO

## ProXR Firmware (USB with AD1 Input)

The `proxr_firmware` directory contains Arduino firmware that enables control of 11 banks of 8 relays (88 relays total) using a dry contact on input AD1.

### Features
- **88 Relays**: 11 banks × 8 relays per bank
- **AD1 Dry Contact Input**: Automatically cycles through relay banks
- **USB Serial Communication**: Program and control at 115200 baud
- **Sequential Switching**: Each AD1 trigger advances to the next bank
- **Manual Control**: Send serial commands for precise control

### Quick Start
1. Open `proxr_firmware/proxr_relay_control.ino` in Arduino IDE
2. Select your board type (typically Arduino Mega 2560)
3. Upload to your NCD ProXR controller via USB
4. Connect dry contact switch to AD1 and GND
5. Each switch activation cycles through relay banks

### Documentation
- [Firmware README](proxr_firmware/README.md) - Complete usage guide
- [Wiring Guide](proxr_firmware/WIRING.md) - Detailed connection instructions
- [Python Tester](proxr_firmware/proxr_tester.py) - Test utility for serial control

## Python Relay Application

The `ncd_relay_app` directory contains a GUI application for controlling relays.

See [ncd_relay_app/README.md](ncd_relay_app/README.md) for details.

## License

This project is licensed under the MIT License.
