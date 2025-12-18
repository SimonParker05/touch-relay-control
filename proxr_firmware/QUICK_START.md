# Quick Start Guide - NCD ProXr Relay Controller

Get up and running with your NCD ProXr relay controller in 5 minutes!

## What You Need

- NCD ProXr Relay Controller (88+ relays)
- USB cable (USB-A to USB-B)
- Dry contact switch (push button, toggle, or reed switch)
- Arduino IDE (download from https://www.arduino.cc/)
- Computer (Windows, Mac, or Linux)

## Step 1: Hardware Setup (2 minutes)

### Connect the Dry Contact Switch

1. Locate the **AD1** pin on your ProXr controller
2. Connect one wire from your switch to **AD1**
3. Connect the other wire from your switch to **GND**

```
   Switch
     |
     ├─── AD1
     |
     └─── GND
```

That's it for wiring! No resistors or additional components needed.

### Connect USB

1. Plug USB cable into ProXr controller
2. Plug other end into your computer
3. Controller should power on (LED indicator if present)

## Step 2: Upload Firmware (2 minutes)

### Install Arduino IDE

1. Download from https://www.arduino.cc/en/software
2. Install on your computer
3. Launch Arduino IDE

### Upload the Sketch

1. Open `proxr_relay_control.ino` in Arduino IDE
2. Select **Tools → Board → Arduino Mega 2560** (or your board type)
3. Select **Tools → Port** → Choose your USB port
   - Windows: COM3, COM4, etc.
   - Mac: /dev/cu.usbmodem... or /dev/cu.usbserial...
   - Linux: /dev/ttyUSB0 or /dev/ttyACM0
4. Click **Upload** button (→)
5. Wait for "Done uploading" message

## Step 3: Test It! (1 minute)

### Open Serial Monitor

1. Click **Tools → Serial Monitor** in Arduino IDE
2. Set baud rate to **115200** (bottom right)
3. You should see:
   ```
   NCD ProXr Relay Controller Initialized
   11 Banks x 8 Relays = 88 Total Relays
   Monitoring AD1 for dry contact input
   ```

### Test the Dry Contact

1. Press/activate your switch connected to AD1
2. You should see: `AD1 Activated - Switched to Bank 1`
3. Press again: `AD1 Activated - Switched to Bank 2`
4. Each press advances to the next bank!

### Test Serial Commands

Type in the serial monitor:

```
BANK 1 ON
```

Press Enter. You should:
- See: `Bank 1 - All Relays ON`
- Hear relays clicking
- See the status: `Bank 1: 11111111`

Turn them off:
```
BANK 1 OFF
```

## How It Works

### Automatic Mode (AD1 Switch)

- **First press**: Turns on Bank 1 (relays 1-8)
- **Second press**: Turns off Bank 1, turns on Bank 2 (relays 9-16)
- **Third press**: Turns off Bank 2, turns on Bank 3 (relays 17-24)
- ...continues through all 11 banks
- **After Bank 11**: Cycles back to Bank 1

### Manual Mode (Serial Commands)

Type commands in the serial monitor:

| Command | Description |
|---------|-------------|
| `BANK 1 ON` | Turn on all 8 relays in Bank 1 |
| `BANK 5 OFF` | Turn off all 8 relays in Bank 5 |
| `RELAY 3 4 ON` | Turn on Relay 4 in Bank 3 |
| `RELAY 7 2 OFF` | Turn off Relay 2 in Bank 7 |
| `STATUS` | Show current state of all relays |
| `ALL OFF` | Turn off all relays |
| `HELP` | Show command help |

## Connect Your Devices

Now that the controller is working, connect your loads (lights, motors, etc.) to the relay terminals:

1. Each relay has 3 terminals: **NO** (Normally Open), **COM** (Common), **NC** (Normally Closed)
2. For most applications, use **COM** and **NO**
3. Connect power source to **COM**
4. Connect load to **NO**
5. When relay turns ON, circuit completes

**⚠️ Safety Warning**: For high voltage (120V/240V), consult a qualified electrician.

## Python Control (Optional)

For advanced automation, use the included Python script:

### Install Python Dependencies
```bash
pip install pyserial
```

### Run Interactive Mode
```bash
python3 proxr_tester.py -p /dev/ttyUSB0
```

### Turn On Bank 3
```bash
python3 proxr_tester.py --bank 3 --on
```

### Run Test Sequence
```bash
python3 proxr_tester.py --test
```

## Common Issues

### "Port not found" or "Access denied"

**Windows**:
- Check Device Manager → Ports (COM & LPT)
- Install CH340 or FTDI drivers if needed

**Linux**:
- Add yourself to dialout group: `sudo usermod -a -G dialout $USER`
- Log out and back in
- Or use: `sudo chmod 666 /dev/ttyUSB0`

**Mac**:
- Check System Information → USB
- Port should appear as /dev/cu.usbmodem* or /dev/cu.usbserial*

### Switch not triggering

1. Check wiring to AD1 and GND
2. Try adjusting `AD1_THRESHOLD` in the code (line 25):
   - Lower value (256) = more sensitive
   - Higher value (768) = less sensitive
3. Add debug: `Serial.println(analogRead(AD1_PIN));` to see readings

### Relays not clicking

1. Ensure USB provides enough power
2. Check if external 12V power supply is needed for your model
3. Verify board type selected in Arduino IDE matches your hardware

## Next Steps

Now that you have the basics working:

1. **Read [README.md](README.md)** - Complete feature documentation
2. **Check [WIRING.md](WIRING.md)** - Detailed wiring diagrams
3. **See [EXAMPLES.md](EXAMPLES.md)** - Practical use cases
4. **Review [CONFIGURATION.md](CONFIGURATION.md)** - Customize for your needs

## Support

- **GitHub Issues**: Report bugs or request features
- **NCD Support**: https://ncd.io/support/ for hardware questions
- **Arduino Forums**: General Arduino help

## Summary

You now have a working relay controller that:
- ✅ Cycles through 11 banks of 8 relays with a simple switch
- ✅ Accepts serial commands for manual control
- ✅ Can be automated with Python scripts
- ✅ Works via USB for power and communication

**Total time**: ~5 minutes from unpacking to working system!

Enjoy your automated relay control! 🎉
