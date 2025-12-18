# NCD ProXr Relay Controller Firmware

This firmware enables control of 11 banks of 8 relays (88 relays total) using an NCD ProXr relay controller with a dry contact input on AD1.

## Features

- **11 Banks × 8 Relays**: Controls 88 relays organized in 11 banks
- **AD1 Dry Contact Input**: Automatically cycles through relay banks when AD1 is activated
- **USB Serial Communication**: Program and control via USB at 115200 baud
- **Sequential Bank Switching**: Each AD1 activation turns off the current bank and turns on the next bank
- **Manual Control**: Send serial commands for precise relay control
- **Status Monitoring**: Query current relay states and system status

## Hardware Requirements

- NCD ProXr Relay Controller (supporting 88+ relays)
- Dry contact switch connected to AD1 input
- USB cable for programming and communication

## Installation

1. **Open Arduino IDE** (version 1.8.x or newer recommended)

2. **Load the Sketch**:
   - Open `proxr_relay_control.ino` in Arduino IDE

3. **Select Board**:
   - Go to Tools → Board
   - Select the appropriate board for your NCD ProXr controller (typically "Arduino Mega 2560" or similar)

4. **Select Port**:
   - Go to Tools → Port
   - Select the USB port connected to your ProXr controller

5. **Upload**:
   - Click the Upload button (→) to compile and upload the firmware
   - Wait for "Done uploading" message

## Configuration

The firmware includes several configurable parameters at the top of the sketch:

```cpp
#define NUM_BANKS 11             // Number of relay banks (default: 11)
#define RELAYS_PER_BANK 8        // Relays per bank (default: 8)
#define AD1_PIN A1               // Analog input pin for dry contact
#define AD1_THRESHOLD 512        // Threshold for contact detection
#define DEBOUNCE_DELAY 50        // Debounce delay in milliseconds
#define BAUD_RATE 115200         // USB Serial baud rate
```

### Adjusting AD1 Threshold

If your dry contact switch is not being detected reliably:

1. Connect to the serial monitor (115200 baud)
2. Temporarily add debug code to print `analogRead(AD1_PIN)` value
3. Adjust `AD1_THRESHOLD` based on the readings (typically 512 for 5V logic)

## Usage

### AD1 Dry Contact Operation

The primary mode of operation uses the dry contact on AD1:

1. **Initial State**: All relays are OFF on startup
2. **First AD1 Activation**: Turns ON all 8 relays in Bank 1
3. **Second AD1 Activation**: Turns OFF Bank 1, turns ON all 8 relays in Bank 2
4. **Subsequent Activations**: Continues cycling through Banks 3-11
5. **After Bank 11**: Cycles back to Bank 1

**Example Sequence**:
- AD1 trigger → Bank 1 ON (Relays 1-8)
- AD1 trigger → Bank 1 OFF, Bank 2 ON (Relays 9-16)
- AD1 trigger → Bank 2 OFF, Bank 3 ON (Relays 17-24)
- ...and so on

### Serial Commands

Connect to the USB serial port at **115200 baud** to send manual commands:

#### Bank Control Commands

```
BANK 1 ON          # Turn on all 8 relays in Bank 1
BANK 5 OFF         # Turn off all 8 relays in Bank 5
BANK 11 ON         # Turn on all 8 relays in Bank 11
```

#### Individual Relay Control

```
RELAY 1 1 ON       # Turn on Relay 1 in Bank 1
RELAY 3 5 OFF      # Turn off Relay 5 in Bank 3
RELAY 11 8 ON      # Turn on Relay 8 in Bank 11
```

#### System Commands

```
STATUS             # Display current state of all relays
ALL OFF            # Turn off all relays in all banks
HELP               # Display command help
```

### Serial Monitor Example

```
NCD ProXr Relay Controller Initialized
11 Banks x 8 Relays = 88 Total Relays
Monitoring AD1 for dry contact input

> STATUS
=== Relay Controller Status ===
Current Active Bank: 1
AD1 State: LOW
Relay States:
Bank 1: 00000000
Bank 2: 00000000
...
Bank 11: 00000000
================================

> BANK 1 ON
Bank 1 - All Relays ON

> STATUS
=== Relay Controller Status ===
Current Active Bank: 1
AD1 State: LOW
Relay States:
Bank 1: 11111111
Bank 2: 00000000
...
```

## Wiring Diagram

### AD1 Dry Contact Connection

```
Dry Contact Switch
    |
    |---- AD1 (Analog Input 1)
    |
   GND
```

The dry contact should connect AD1 to ground when closed. The internal pull-up resistor keeps AD1 HIGH when the contact is open.

### USB Connection

Connect the USB cable from your computer to the ProXr controller's USB port. This provides:
- Power to the controller
- Serial communication for programming and control
- Status monitoring

## Troubleshooting

### Issue: AD1 not triggering bank switching

**Solutions**:
1. Check dry contact wiring (should connect AD1 to GND when closed)
2. Adjust `AD1_THRESHOLD` value (try values between 256-768)
3. Verify contact is properly debounced (default 50ms)
4. Check serial monitor for "AD1 Activated" messages

### Issue: Relays not responding

**Solutions**:
1. Verify ProXr controller is properly powered
2. Check USB connection and serial communication
3. Ensure correct board type selected in Arduino IDE
4. Verify bank/relay numbers are within valid ranges (1-11, 1-8)

### Issue: Firmware won't upload

**Solutions**:
1. Check USB cable connection
2. Verify correct COM port selected in Arduino IDE
3. Ensure no other serial programs are using the port
4. Try pressing reset button on controller before upload

## NCD ProXr Protocol

This firmware uses the NCD ProXr binary protocol:

- **Command Format**: `[0xFE] [COMMAND] [BANK] [CHECKSUM]`
- **Commands Used**:
  - `0x64`: Turn relay ON (bank addressing)
  - `0x65`: Turn relay OFF (bank addressing)
  - `0x66`: Turn all relays ON in a bank
  - `0x67`: Turn all relays OFF in a bank

## Technical Specifications

- **Communication**: USB Serial @ 115200 baud
- **Input**: AD1 analog input with 512 threshold
- **Debounce**: 50ms for contact stability
- **Relay Banks**: 11 banks configurable
- **Relays per Bank**: 8 relays configurable
- **Total Relays**: 88 (11 × 8)
- **Cycle Behavior**: Sequential with wraparound

## License

This project is licensed under the MIT License.

## Support

For issues or questions about NCD ProXr controllers, visit:
- [NCD.io Support](https://ncd.io/support/)
- [NCD ProXr Documentation](https://ncd.io/proxr-relay-controllers/)
