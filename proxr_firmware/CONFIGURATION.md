# NCD ProXr Configuration Guide

This guide helps you customize the firmware for different hardware configurations and use cases.

## Configuration Parameters

All configuration is done by editing constants at the top of `proxr_relay_control.ino`:

```cpp
// Configuration
#define NUM_BANKS 11             // Number of relay banks
#define RELAYS_PER_BANK 8        // 8 relays per bank
#define AD1_PIN A1               // Analog input AD1 for dry contact
#define AD1_THRESHOLD 512        // Threshold for dry contact detection
#define DEBOUNCE_DELAY 50        // Debounce delay in milliseconds
#define BAUD_RATE 115200         // USB Serial baud rate
```

## Common Configuration Scenarios

### Scenario 1: Different Number of Banks

If you have fewer or more relay banks:

**Example: 8 banks instead of 11**
```cpp
#define NUM_BANKS 8
```

**Example: 16 banks**
```cpp
#define NUM_BANKS 16
```

**Note**: Ensure your ProXr hardware supports the number of relays (NUM_BANKS × RELAYS_PER_BANK)

### Scenario 2: Different Relays Per Bank

Some ProXr models have different relay configurations:

**4 relays per bank**
```cpp
#define RELAYS_PER_BANK 4
```

**16 relays per bank**
```cpp
#define RELAYS_PER_BANK 16
```

**Custom configuration examples**:
- 4 banks × 16 relays = 64 relays total
- 8 banks × 8 relays = 64 relays total
- 11 banks × 8 relays = 88 relays total (default)

### Scenario 3: Different Input Pin

If using a different analog input:

**AD0 instead of AD1**
```cpp
#define AD1_PIN A0
```

**AD2**
```cpp
#define AD1_PIN A2
```

**Digital pin (if preferred)**
```cpp
#define AD1_PIN 2              // Digital pin 2
// Note: Change analogRead() to digitalRead() in code
```

### Scenario 4: Adjust Contact Detection Threshold

The threshold determines when a dry contact is considered "activated".

**Lower threshold (more sensitive)**
```cpp
#define AD1_THRESHOLD 256      // Triggers at ~1.25V
```

**Higher threshold (less sensitive)**
```cpp
#define AD1_THRESHOLD 768      // Triggers at ~3.75V
```

**Finding the right value**:
1. Add debug code to print analog value:
   ```cpp
   Serial.println(analogRead(AD1_PIN));
   ```
2. Observe values when switch is open and closed
3. Set threshold midway between the two states

**Typical values**:
- Open circuit: ~1023 (5V)
- Closed to ground: ~0 (0V)
- Threshold: 512 (mid-point)

### Scenario 5: Adjust Debounce Delay

Increase if you experience:
- Multiple triggers from single button press
- Erratic behavior with mechanical switches
- Contact bounce issues

**More debounce (slower but more stable)**
```cpp
#define DEBOUNCE_DELAY 100     // 100ms
```

**Less debounce (faster but may be unstable)**
```cpp
#define DEBOUNCE_DELAY 20      // 20ms (minimum recommended)
```

**Guidelines**:
- Push buttons: 50-100ms typically sufficient
- Toggle switches: 20-50ms usually enough
- Reed switches: 20ms often adequate
- Noisy environment: 100-200ms may be needed

### Scenario 6: Different Baud Rate

Change if you need compatibility with existing systems:

**Standard rates**
```cpp
#define BAUD_RATE 9600         // Slower, very compatible
#define BAUD_RATE 19200        // Common alternative
#define BAUD_RATE 57600        // Fast
#define BAUD_RATE 115200       // Very fast (default)
```

**Note**: Update your serial terminal and Python scripts to match

## Hardware-Specific Configurations

### ProXr Nano (Smaller Board)

```cpp
#define NUM_BANKS 4
#define RELAYS_PER_BANK 4
#define BAUD_RATE 115200
```

### ProXr 32-Relay Board

```cpp
#define NUM_BANKS 4
#define RELAYS_PER_BANK 8
#define BAUD_RATE 115200
```

### ProXr 64-Relay Board

```cpp
#define NUM_BANKS 8
#define RELAYS_PER_BANK 8
#define BAUD_RATE 115200
```

### Custom High-Density Setup (128 relays)

```cpp
#define NUM_BANKS 16
#define RELAYS_PER_BANK 8
#define BAUD_RATE 115200
```

## Behavioral Modifications

### Change 1: Skip Banks (Every Other Bank)

Modify `handleAD1Activation()`:

```cpp
void handleAD1Activation() {
  turnOffBank(currentBank);
  
  // Move to next bank (skip one)
  currentBank = (currentBank + 2) % NUM_BANKS;
  
  turnOnBank(currentBank);
  
  Serial.print("AD1 Activated - Switched to Bank ");
  Serial.println(currentBank + 1);
}
```

### Change 2: Toggle Single Bank (No Cycling)

Modify to toggle one bank on/off instead of cycling:

```cpp
void handleAD1Activation() {
  // Toggle bank 1 on/off
  if (relayStates[0][0]) {  // If bank 1 is on
    turnOffBank(0);
  } else {
    turnOnBank(0);
  }
}
```

### Change 3: Momentary Activation (Auto-Off)

Turn bank on, wait, then turn off automatically:

```cpp
void handleAD1Activation() {
  turnOffBank(currentBank);
  currentBank = (currentBank + 1) % NUM_BANKS;
  turnOnBank(currentBank);
  
  delay(5000);  // Keep on for 5 seconds
  
  turnOffBank(currentBank);
  Serial.println("Bank auto-off after 5 seconds");
}
```

### Change 4: All Banks On/Off Toggle

Instead of cycling, turn all banks on or all off:

```cpp
bool allBanksOn = false;

void handleAD1Activation() {
  if (allBanksOn) {
    turnOffAllRelays();
    allBanksOn = false;
    Serial.println("All banks OFF");
  } else {
    for (int bank = 0; bank < NUM_BANKS; bank++) {
      turnOnBank(bank);
    }
    allBanksOn = true;
    Serial.println("All banks ON");
  }
}
```

## Protocol Modifications

### Use Different ProXr Commands

The firmware uses these NCD ProXr commands:

```cpp
#define CMD_PREFIX 0xFE          // Command prefix
#define RELAY_ON 0x64            // Turn relay ON
#define RELAY_OFF 0x65           // Turn relay OFF
#define RELAY_ON_ALL 0x66        // Turn all ON in bank
#define RELAY_OFF_ALL 0x67       // Turn all OFF in bank
```

**For different ProXr models**, consult NCD documentation and update accordingly.

### Add Status Query Commands

To query relay status from ProXr (if supported):

```cpp
#define RELAY_STATUS 0x68        // Query relay status

void queryRelayStatus(byte bank) {
  sendProXrCommand(RELAY_STATUS, bank);
}
```

## Input Modifications

### Use Digital Input Instead of Analog

Change from analog to digital input:

```cpp
// In setup()
pinMode(AD1_PIN, INPUT_PULLUP);  // Use internal pull-up

// In loop()
bool currentAD1State = !digitalRead(AD1_PIN);  // Invert because pull-up
```

### Use Multiple Inputs

Add support for multiple dry contact inputs:

```cpp
#define AD1_PIN A1
#define AD2_PIN A2

// In loop()
int ad1Value = analogRead(AD1_PIN);
int ad2Value = analogRead(AD2_PIN);

bool ad1Active = (ad1Value > AD1_THRESHOLD);
bool ad2Active = (ad2Value > AD1_THRESHOLD);

if (ad1Active) {
  handleAD1Activation();  // Next bank
}

if (ad2Active) {
  handleAD2Activation();  // Previous bank
}
```

### Add Direction Control (Forward/Backward)

Two buttons for forward and backward cycling:

```cpp
#define BTN_NEXT A1
#define BTN_PREV A2

void handleNextButton() {
  turnOffBank(currentBank);
  currentBank = (currentBank + 1) % NUM_BANKS;
  turnOnBank(currentBank);
}

void handlePrevButton() {
  turnOffBank(currentBank);
  currentBank = (currentBank - 1 + NUM_BANKS) % NUM_BANKS;
  turnOnBank(currentBank);
}
```

## Testing Configurations

After modifying configuration:

1. **Compile Check**
   - Arduino IDE: Click Verify (✓)
   - Look for compilation errors
   - Fix any issues

2. **Upload**
   - Connect ProXr via USB
   - Select correct board type
   - Upload firmware

3. **Serial Monitor Test**
   - Open Serial Monitor (115200 baud)
   - Look for startup messages
   - Send "STATUS" command
   - Send "HELP" command

4. **AD1 Input Test**
   - Trigger dry contact
   - Observe serial messages
   - Verify bank changes

5. **Relay Output Test**
   - Send "BANK 1 ON"
   - Listen for relay clicks
   - Verify correct relays activate

## Configuration Examples by Application

### Building Automation

```cpp
#define NUM_BANKS 10            // 10 floors
#define RELAYS_PER_BANK 8       // 8 zones per floor
#define AD1_THRESHOLD 512
#define DEBOUNCE_DELAY 100      // Building switches can be noisy
#define BAUD_RATE 9600          // Compatible with building systems
```

### Manufacturing Line

```cpp
#define NUM_BANKS 15            // 15 process stages
#define RELAYS_PER_BANK 4       // 4 machines per stage
#define AD1_THRESHOLD 512
#define DEBOUNCE_DELAY 50
#define BAUD_RATE 115200        // Fast communication
```

### Agricultural Irrigation

```cpp
#define NUM_BANKS 8             // 8 field zones
#define RELAYS_PER_BANK 8       // 8 valves per zone
#define AD1_THRESHOLD 512
#define DEBOUNCE_DELAY 200      // Outdoor, may be noisy
#define BAUD_RATE 9600          // Long cable runs
```

### Home Automation

```cpp
#define NUM_BANKS 6             // 6 rooms
#define RELAYS_PER_BANK 8       // 8 devices per room
#define AD1_THRESHOLD 512
#define DEBOUNCE_DELAY 50
#define BAUD_RATE 115200        // Fast response
```

## Backup Configuration

Before making changes, always document your working configuration:

```cpp
/* 
 * Working Configuration - 2024-12-18
 * Hardware: ProXr 88-relay board
 * Application: Building lighting control
 * Tested and verified
 */
#define NUM_BANKS 11
#define RELAYS_PER_BANK 8
#define AD1_PIN A1
#define AD1_THRESHOLD 512
#define DEBOUNCE_DELAY 50
#define BAUD_RATE 115200
```

## Troubleshooting Configuration Issues

### Problem: Wrong Number of Relays Activate

**Check**:
- `RELAYS_PER_BANK` matches hardware
- `NUM_BANKS` is correct

### Problem: AD1 Doesn't Trigger

**Check**:
- `AD1_PIN` matches wiring
- `AD1_THRESHOLD` is appropriate
- Add debug: `Serial.println(analogRead(AD1_PIN));`

### Problem: Bouncing/Multiple Triggers

**Check**:
- Increase `DEBOUNCE_DELAY`
- Check switch quality

### Problem: Serial Commands Don't Work

**Check**:
- `BAUD_RATE` matches terminal
- USB cable is good
- Correct COM port selected

## Summary

Key configuration parameters:
1. **NUM_BANKS** - Number of relay banks
2. **RELAYS_PER_BANK** - Relays in each bank
3. **AD1_PIN** - Input pin for dry contact
4. **AD1_THRESHOLD** - Trigger threshold for input
5. **DEBOUNCE_DELAY** - Switch debounce time
6. **BAUD_RATE** - Serial communication speed

Modify these to match your hardware and requirements!
