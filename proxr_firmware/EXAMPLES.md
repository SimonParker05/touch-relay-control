# NCD ProXr Relay Controller - Usage Examples

This document provides practical examples for using the ProXr relay controller firmware.

## Table of Contents
1. [Basic Operation](#basic-operation)
2. [Serial Commands](#serial-commands)
3. [Python Tester Script](#python-tester-script)
4. [Common Use Cases](#common-use-cases)
5. [Troubleshooting Examples](#troubleshooting-examples)

## Basic Operation

### Scenario 1: Touch-Activated Sequential Bank Control

**Setup**: A dry contact switch connected to AD1 is used to cycle through relay banks.

**Use Case**: Sequential control of 11 different zones (lighting, HVAC, etc.)

**Operation**:
1. System starts with all relays OFF
2. First touch of switch → Bank 1 turns ON (relays 1-8)
3. Second touch → Bank 1 turns OFF, Bank 2 turns ON (relays 9-16)
4. Continue touching to cycle through all 11 banks
5. After Bank 11 → cycles back to Bank 1

**No programming needed** - just wire the dry contact and touch!

### Scenario 2: Momentary Push Button Control

**Hardware**: Momentary push button wired to AD1

```
    Push Button
    ┌─────┐
    │  ○  │
    └──┬──┘
       │
   AD1 ○────┤├──── GND
```

**Result**: Each button press advances to the next bank.

### Scenario 3: Magnetic Reed Switch

**Hardware**: Reed switch activated by magnet proximity

**Application**: Door opening triggers bank change
- Magnet on door, reed switch on frame
- Door opens → magnet moves away → switch changes
- Bank advances when door opens

## Serial Commands

### Opening Serial Connection

**Windows (PuTTY)**:
1. Select "Serial" connection type
2. Serial line: `COM3` (or your port)
3. Speed: `115200`
4. Click "Open"

**Linux/Mac (screen)**:
```bash
screen /dev/ttyUSB0 115200
```

**Linux/Mac (minicom)**:
```bash
minicom -D /dev/ttyUSB0 -b 115200
```

### Example Serial Sessions

#### Session 1: Testing All Banks

```
> HELP
=== NCD ProXr Relay Controller Commands ===
BANK <1-11> ON/OFF   - Turn all relays in a bank ON or OFF
...

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

> BANK 1 OFF
Bank 1 - All Relays OFF

> BANK 2 ON
Bank 2 - All Relays ON
```

#### Session 2: Individual Relay Control

```
> RELAY 1 1 ON
Relay 1 in Bank 1 - ON

> RELAY 1 5 ON
Relay 5 in Bank 1 - ON

> STATUS
=== Relay Controller Status ===
...
Bank 1: 10001000
...

> RELAY 1 1 OFF
Relay 1 in Bank 1 - OFF

> RELAY 1 5 OFF
Relay 5 in Bank 1 - OFF
```

#### Session 3: Emergency All Off

```
> ALL OFF
Turning off all relays...
Bank 1 - All Relays OFF
Bank 2 - All Relays OFF
...
Bank 11 - All Relays OFF
```

## Python Tester Script

### Example 1: Interactive Mode

```bash
$ python3 proxr_tester.py -p /dev/ttyUSB0

Connected to /dev/ttyUSB0 at 115200 baud
Controller: NCD ProXr Relay Controller Initialized
Controller: 11 Banks x 8 Relays = 88 Total Relays
Controller: Monitoring AD1 for dry contact input

=== Interactive Mode ===
Enter commands or type 'exit' to quit
Type 'help' for available commands

ProXr> STATUS

Getting status...
=== Relay Controller Status ===
Current Active Bank: 1
AD1 State: LOW
...

ProXr> BANK 3 ON

Turning ON Bank 3...
Bank 3 - All Relays ON

ProXr> exit
Exiting...
Serial connection closed
```

### Example 2: Command Line Operations

**Turn on Bank 5**:
```bash
python3 proxr_tester.py --bank 5 --on
```

**Turn off Bank 5**:
```bash
python3 proxr_tester.py --bank 5 --off
```

**Turn on Relay 3 in Bank 7**:
```bash
python3 proxr_tester.py --relay 7 3 --on
```

**Get Status**:
```bash
python3 proxr_tester.py --status
```

**Emergency All Off**:
```bash
python3 proxr_tester.py --all-off
```

### Example 3: Automated Test Sequence

```bash
python3 proxr_tester.py --test

=== Running Test Sequence ===
This will cycle through all 11 banks

Turning OFF all relays...

--- Testing Bank 1 ---
Turning ON Bank 1...
Bank 1 - All Relays ON

Turning OFF Bank 1...
Bank 1 - All Relays OFF

--- Testing Bank 2 ---
...
```

### Example 4: Custom Port

**Windows**:
```bash
python3 proxr_tester.py -p COM3
```

**Linux (ACM device)**:
```bash
python3 proxr_tester.py -p /dev/ttyACM0
```

**Mac**:
```bash
python3 proxr_tester.py -p /dev/cu.usbmodem14101
```

## Common Use Cases

### Use Case 1: Building Lighting Control

**Scenario**: 11 floors, 8 light zones per floor

**Setup**:
- Each bank controls one floor (8 zones)
- Dry contact is a master control switch
- Each switch press cycles to next floor

**Operation**:
```bash
# Via Python script - turn on floor 3
python3 proxr_tester.py --bank 3 --on

# Via serial - turn on specific zone
RELAY 3 5 ON    # Floor 3, Zone 5
```

**Automation**: Use cron or scheduler to control times
```bash
# Morning - turn on floor 1
0 7 * * * /usr/bin/python3 /path/to/proxr_tester.py --bank 1 --on

# Evening - all off
0 22 * * * /usr/bin/python3 /path/to/proxr_tester.py --all-off
```

### Use Case 2: Irrigation System

**Scenario**: 11 zones, 8 valves per zone

**Bank Assignment**:
- Bank 1: Front yard zones
- Bank 2: Back yard zones
- Bank 3: Garden zones
- etc.

**Control**:
```python
# Python automation script
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

def water_zone(bank, duration_minutes):
    """Water a zone for specified duration"""
    # Turn on bank
    ser.write(f"BANK {bank} ON\n".encode())
    print(f"Watering bank {bank} for {duration_minutes} minutes")
    
    # Wait
    time.sleep(duration_minutes * 60)
    
    # Turn off bank
    ser.write(f"BANK {bank} OFF\n".encode())
    print(f"Bank {bank} watering complete")

# Water front yard for 15 minutes
water_zone(1, 15)

# Water back yard for 20 minutes
water_zone(2, 20)
```

### Use Case 3: Manufacturing Process Control

**Scenario**: Sequential machine activation

**Process**:
1. Bank 1: Preparation machines
2. Bank 2: Processing stage 1
3. Bank 3: Processing stage 2
...
11. Bank 11: Packaging

**Control**: AD1 connected to PLC or process controller output
- Process controller triggers AD1 when stage completes
- Automatically advances to next stage

### Use Case 4: Server Room Power Management

**Scenario**: 88 power outlets for servers/equipment

**Banks**:
- Banks 1-6: Development servers
- Banks 7-9: Production servers
- Bank 10: Network equipment
- Bank 11: Backup systems

**Usage**:
```bash
# Scheduled maintenance - power down dev servers
python3 proxr_tester.py --bank 1 --off
python3 proxr_tester.py --bank 2 --off
# ... etc

# Power cycle specific server (Bank 3, Relay 4)
python3 proxr_tester.py --relay 3 4 --off
sleep 10
python3 proxr_tester.py --relay 3 4 --on
```

## Troubleshooting Examples

### Problem 1: AD1 Not Triggering

**Test AD1 Connection**:
```bash
# Connect to serial monitor
screen /dev/ttyUSB0 115200

# Manually connect a wire between AD1 and GND
# Should see: "AD1 Activated - Switched to Bank X"
```

**If no message appears**:
- Check wiring
- Verify switch actually closes
- Adjust `AD1_THRESHOLD` in firmware (try 256 or 768)

### Problem 2: Relay Not Clicking

**Test Individual Relay**:
```bash
# Via Python
python3 proxr_tester.py --relay 1 1 --on

# Via Serial
screen /dev/ttyUSB0 115200
> RELAY 1 1 ON
```

**If relay doesn't click**:
- Check power supply
- Verify relay number is valid (1-11, 1-8)
- Listen carefully - click is often quiet

### Problem 3: Lost Connection

**Reconnect**:
```bash
# List available ports (Linux)
ls /dev/tty* | grep -E "(USB|ACM)"

# List ports (Mac)
ls /dev/cu.*

# Windows - check Device Manager → Ports (COM & LPT)
```

**Test Connection**:
```bash
# Simple echo test
python3 -c "
import serial
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=2)
ser.write(b'HELP\n')
print(ser.read(1000).decode())
"
```

### Problem 4: Wrong Bank Activates

**Check Current State**:
```bash
python3 proxr_tester.py --status
```

**Reset to Known State**:
```bash
# Turn off all relays
python3 proxr_tester.py --all-off

# Turn on desired bank
python3 proxr_tester.py --bank 1 --on
```

### Problem 5: Rapid Bank Switching

If AD1 triggers too quickly (contact bounce):

**Solution**: Increase debounce delay in firmware
```cpp
#define DEBOUNCE_DELAY 100  // Increase from 50 to 100ms
```

## Advanced Examples

### Web-Based Control (Flask)

```python
from flask import Flask, request
import serial

app = Flask(__name__)
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

@app.route('/bank/<int:bank>/<state>')
def control_bank(bank, state):
    if state.upper() in ['ON', 'OFF']:
        cmd = f"BANK {bank} {state.upper()}\n"
        ser.write(cmd.encode())
        return f"Bank {bank} turned {state}"
    return "Invalid state", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Usage**:
```bash
# Turn on bank 5
curl http://localhost:5000/bank/5/on

# Turn off bank 5
curl http://localhost:5000/bank/5/off
```

### MQTT Integration

```python
import paho.mqtt.client as mqtt
import serial

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

def on_message(client, userdata, msg):
    # Topic: proxr/bank/1/command
    # Payload: ON or OFF
    parts = msg.topic.split('/')
    bank = parts[2]
    command = msg.payload.decode()
    
    ser.write(f"BANK {bank} {command}\n".encode())
    print(f"Bank {bank} set to {command}")

client = mqtt.Client()
client.on_message = on_message
client.connect("mqtt.example.com", 1883, 60)
client.subscribe("proxr/bank/+/command")
client.loop_forever()
```

## Summary

The ProXr relay controller provides flexible control options:

1. **Simple**: Just wire a dry contact to AD1 - no programming needed
2. **Manual**: Send text commands via serial terminal
3. **Scripted**: Use Python tester for automation
4. **Advanced**: Integrate with web, MQTT, or other systems

Choose the method that best fits your application!
