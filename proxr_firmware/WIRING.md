# NCD ProXr Relay Controller - Wiring Guide

This document provides detailed wiring instructions for the NCD ProXr relay controller with AD1 dry contact input.

## Overview

The system consists of:
- **NCD ProXr Relay Controller** (88 relay capacity minimum)
- **Dry Contact Switch** (connected to AD1)
- **USB Cable** (for programming and power)
- **Relay Load Connections** (devices controlled by relays)

## Pin Connections

### AD1 Dry Contact Input

The AD1 (Analog Digital Input 1) is used to detect the dry contact switch activation.

```
┌─────────────────────────┐
│  ProXr Controller       │
│                         │
│  AD1 ○────────┐         │
│               │         │
│  GND ○────────┼─────┐   │
└───────────────┼─────┼───┘
                │     │
                │     │
         ┌──────┴─────┴──────┐
         │   Dry Contact      │
         │     Switch         │
         └────────────────────┘
```

**Wiring Steps:**
1. Connect one terminal of your dry contact switch to **AD1** on the ProXr controller
2. Connect the other terminal of the switch to **GND** (ground)
3. When the switch closes, it connects AD1 to ground
4. The firmware uses a threshold to detect this connection

**Important Notes:**
- No external resistor needed - firmware uses internal pull-up
- AD1 is HIGH when switch is open (default state)
- AD1 goes LOW when switch is closed (activated state)
- Firmware includes 50ms debounce for switch stability

### USB Connection

```
┌─────────────────────────┐
│  ProXr Controller       │
│                         │
│     USB Port            │
│       ○○○○○             │
└─────────┼───────────────┘
          │
          │ USB Cable
          │
     ┌────┴─────┐
     │ Computer │
     └──────────┘
```

**USB Provides:**
- Power to the controller
- Serial communication (115200 baud)
- Programming interface
- Status monitoring

## Relay Bank Configuration

The system controls **11 banks of 8 relays each** (88 relays total):

```
Bank 1:  Relays 1-8
Bank 2:  Relays 9-16
Bank 3:  Relays 17-24
Bank 4:  Relays 25-32
Bank 5:  Relays 33-40
Bank 6:  Relays 41-48
Bank 7:  Relays 49-56
Bank 8:  Relays 57-64
Bank 9:  Relays 65-72
Bank 10: Relays 73-80
Bank 11: Relays 81-88
```

## Relay Load Connections

Each relay on the NCD ProXr controller typically has three terminals:

```
     Relay Terminal Block
     ┌─────────────────┐
     │  NO  COM  NC    │
     │  ○    ○    ○    │
     └──┼────┼────┼────┘
        │    │    │
```

**Terminal Types:**
- **NO** (Normally Open): Connected to COM when relay is ON
- **COM** (Common): The switching point
- **NC** (Normally Closed): Connected to COM when relay is OFF

### Example Load Connection (Normally Open)

```
┌─────────┐         ┌─────────┐
│ Power   │         │  Load   │
│ Source  │         │ (Device)│
└────┬────┘         └────┬────┘
     │                   │
     │    Relay          │
     └─────COM    NO─────┘
           ○       ○
```

**Wiring Steps for Each Relay:**
1. Connect power source to **COM** terminal
2. Connect load (device) to **NO** terminal
3. Connect other side of load to power source return/ground
4. When relay turns ON, circuit completes and device operates

### High Current Applications

For high current loads:
- Use external contactors triggered by ProXr relays
- ProXr relay controls contactor coil
- Contactor handles high current load

```
ProXr Relay              Contactor
┌─────────┐            ┌──────────┐
│ NO  COM │            │ Coil +   │
│ ○───○   │            │ ○─┐      │
└─────┬───┘            └───┼──────┘
      │                    │
      └────────────────────┘
      
Contactor Contacts       High Current Load
┌──────────────┐        ┌─────────┐
│ NO      COM  │        │  Motor  │
│ ○───────○    │        │ or Lamp │
└──┬──────┬────┘        └────┬────┘
   │      └──────────────────┘
   └─── High Current Source
```

## Dry Contact Switch Types

The AD1 input works with various dry contact switch types:

### 1. Push Button (Momentary)
```
  ┌───┐
  │ ○ │ Push Button
  └─┬─┘
    │
```
- Brief closure on each press
- Firmware advances to next bank on each press

### 2. Toggle Switch (Maintained)
```
  ┌─○─┐
  │ │ │ Toggle Switch
  └─┴─┘
```
- Stays in position after actuation
- Each toggle changes bank

### 3. Reed Switch (Magnetic)
```
  ┌───┐
  │▯▯▯│ Reed Switch
  └───┘
```
- Activates when magnet approaches
- Good for door/position sensing

### 4. Proximity Sensor (Dry Contact Output)
```
  ┌─────┐
  │ [◉] │ Proximity Sensor
  └─────┘
```
- NO/NC relay output
- Wire NO contacts to AD1 and GND

### 5. Relay Contact (From Another System)
```
  ┌─────┐
  │Relay│
  │NO-CM│
  └─────┘
```
- Use relay contacts as trigger
- Isolates from other systems

## Complete System Diagram

```
                    ┌──────────────────────────────────┐
                    │   NCD ProXr Relay Controller     │
                    │                                  │
  USB to Computer   │  USB   AD1  GND                  │
        ├───────────┤  Port   ○    ○                   │
                    │          │    │                   │
                    │  ┌───────┴────┴───────────┐      │
                    │  │  Firmware Control      │      │
  Dry Contact ──────┤  │  - Debounce           │      │
  Switch            │  │  - Bank Switching     │      │
                    │  │  - Serial Commands    │      │
                    │  └───────────────────────┘      │
                    │                                  │
                    │  Relay Banks 1-11 (8 each)      │
                    │  ┌────┬────┬────┬─────────┐     │
                    │  │ B1 │ B2 │ B3 │   ...   │     │
                    │  │1-8 │9-16│17-24│  81-88  │     │
                    │  └─┬──┴─┬──┴─┬──┴─────────┘     │
                    └────┼────┼────┼─────────────────┘
                         │    │    │
                    ┌────┴────┴────┴─────┐
                    │   Load Devices     │
                    │ (Lights, Motors,   │
                    │  Pumps, etc.)      │
                    └────────────────────┘
```

## Power Considerations

### Controller Power
- USB provides 5V power for controller logic
- Sufficient for typical ProXr operation
- For high relay count or external power requirements, use external 12V supply

### Relay Load Power
- Relay loads require **separate power source**
- Do NOT power high current loads from USB
- Common voltages: 12V, 24V, 120VAC, 240VAC
- Check ProXr relay ratings for your application

### Voltage Ratings (Typical NCD ProXr)
- Relay Contact Rating: 10A @ 250VAC / 30VDC
- Coil Voltage: 5V or 12V (model dependent)
- Logic Level: 3.3V or 5V

## Safety Guidelines

⚠️ **IMPORTANT SAFETY WARNINGS:**

1. **Electrical Safety**
   - Always disconnect power before wiring
   - Use appropriate wire gauge for current
   - Follow local electrical codes
   - Use proper insulation and enclosures

2. **Relay Ratings**
   - Never exceed relay current/voltage ratings
   - Use appropriate fuses or circuit breakers
   - Consider inrush current for motors/lamps

3. **High Voltage**
   - If using mains voltage (120VAC/240VAC):
     - Use qualified electrician
     - Follow all safety codes
     - Use proper enclosures
     - Label all connections

4. **Isolation**
   - Keep low voltage (USB, AD1) isolated from high voltage
   - Use separate enclosures if necessary
   - Proper grounding is essential

## Testing Procedure

### 1. Initial Hardware Test
```
1. Connect USB cable only (no loads)
2. Upload firmware
3. Open serial monitor (115200 baud)
4. Verify startup messages appear
5. Send "HELP" command - verify response
```

### 2. AD1 Input Test
```
1. With serial monitor open
2. Manually connect AD1 to GND with wire
3. Should see "AD1 Activated - Switched to Bank X"
4. Disconnect and reconnect to test multiple times
5. Verify bank number increments
```

### 3. Relay Output Test (No Load)
```
1. Send "BANK 1 ON" via serial
2. Listen for relay click sounds
3. Send "BANK 1 OFF"
4. Verify relays turn off
5. Test each bank individually
```

### 4. Load Test (Start with Low Power)
```
1. Connect a small LED with resistor to one relay
2. Turn on that specific relay
3. Verify LED lights up
4. Test with progressively larger loads
5. Always use fuses/breakers
```

## Troubleshooting

### AD1 Not Responding
- Check continuity of wiring
- Try different AD1_THRESHOLD value in firmware
- Verify switch is actually closing
- Check for proper ground connection

### Relays Not Clicking
- Verify USB power is sufficient
- Check if external power supply needed
- Test with "STATUS" command to see states
- Verify proper board type in Arduino IDE

### Intermittent Operation
- Check all wiring connections are secure
- Increase DEBOUNCE_DELAY if needed
- Ensure USB cable is good quality
- Check for electrical noise/interference

## Recommended Components

- **Dry Contact Switch**: SPST momentary push button, 5A rating
- **USB Cable**: USB-A to USB-B, 3-6 feet, shielded
- **Wire**: 22-18 AWG for control signals, appropriate gauge for loads
- **Fuses**: Match to relay and load current ratings
- **Enclosure**: NEMA rated for environment
- **Terminal Blocks**: For organized connections

## Maintenance

1. **Regular Checks**
   - Inspect wiring for damage
   - Test relays periodically
   - Check for corrosion on terminals
   - Verify switch operation

2. **Relay Lifespan**
   - Relays have finite mechanical life
   - Typical: 100,000-1,000,000 operations
   - Monitor for failures
   - Replace as needed

3. **Software Updates**
   - Keep firmware updated
   - Test thoroughly after updates
   - Keep backup of working configuration

## Additional Resources

- NCD ProXr Product Documentation: https://ncd.io/proxr-relay-controllers/
- Arduino IDE: https://www.arduino.cc/en/software
- Serial Terminal Software: PuTTY, minicom, screen
- Project Repository: [Your repository URL]

## Support

For technical support:
1. Check this wiring guide
2. Review firmware README.md
3. Test with provided Python tester script
4. Contact NCD.io support for hardware issues
5. Open GitHub issue for firmware problems
