/*
 * NCD ProXr Relay Controller with AD1 Dry Contact Input
 * 
 * This firmware controls 11 banks of 8 relays (88 relays total) using
 * a dry contact input on AD1. When AD1 is activated, it cycles through
 * the relay banks sequentially.
 * 
 * Hardware: NCD ProXr Relay Controller
 * Communication: USB Serial
 * Input: AD1 (Dry Contact)
 * Relays: 11 banks × 8 relays = 88 relays total
 */

// NCD ProXr Command Definitions
// Protocol format: [0xFE] [COMMAND] [DATA] [CHECKSUM]
// Checksum = 255 - (sum of all bytes) + 1
// Note: ProXr uses 1-based numbering (banks 1-11, relays 1-88)
#define CMD_PREFIX 0xFE          // Command prefix for ProXr
#define RELAY_ON 0x64            // Turn relay ON (individual relay 1-88)
#define RELAY_OFF 0x65           // Turn relay OFF (individual relay 1-88)
#define RELAY_ON_ALL 0x66        // Turn all relays ON in a bank (bank 1-11)
#define RELAY_OFF_ALL 0x67       // Turn all relays OFF in a bank (bank 1-11)

// Configuration
#define NUM_BANKS 11             // 11 banks of relays
#define RELAYS_PER_BANK 8        // 8 relays per bank
#define AD1_PIN A1               // Analog input AD1 for dry contact
#define AD1_THRESHOLD 512        // Threshold for dry contact detection
#define DEBOUNCE_DELAY 50        // Debounce delay in milliseconds
#define BAUD_RATE 115200         // USB Serial baud rate

// State variables
int currentBank = 0;             // Current active bank (0-10)
bool lastAD1State = false;       // Previous state of AD1 input
unsigned long lastDebounceTime = 0; // Last time AD1 state changed
bool relayStates[NUM_BANKS][RELAYS_PER_BANK]; // Track relay states

void setup() {
  // Initialize USB Serial communication
  Serial.begin(BAUD_RATE);
  
  // Initialize AD1 pin as input
  pinMode(AD1_PIN, INPUT);
  
  // Initialize relay states (all OFF)
  for (int bank = 0; bank < NUM_BANKS; bank++) {
    for (int relay = 0; relay < RELAYS_PER_BANK; relay++) {
      relayStates[bank][relay] = false;
    }
  }
  
  // Turn off all relays on startup
  turnOffAllRelays();
  
  // Send ready message
  Serial.println("NCD ProXr Relay Controller Initialized");
  Serial.println("11 Banks x 8 Relays = 88 Total Relays");
  Serial.println("Monitoring AD1 for dry contact input");
}

void loop() {
  // Read AD1 input
  int ad1Value = analogRead(AD1_PIN);
  bool currentAD1State = (ad1Value > AD1_THRESHOLD);
  
  // Check for state change with debouncing
  if (currentAD1State != lastAD1State) {
    lastDebounceTime = millis();
  }
  
  if ((millis() - lastDebounceTime) > DEBOUNCE_DELAY) {
    // If AD1 state has been stable for debounce delay
    if (currentAD1State && !lastAD1State) {
      // Rising edge detected - AD1 activated
      handleAD1Activation();
    }
  }
  
  lastAD1State = currentAD1State;
  
  // Check for serial commands
  if (Serial.available() > 0) {
    processSerialCommand();
  }
  
  delay(10); // Small delay for stability
}

void handleAD1Activation() {
  // Turn off current bank
  turnOffBank(currentBank);
  
  // Move to next bank
  currentBank = (currentBank + 1) % NUM_BANKS;
  
  // Turn on new bank
  turnOnBank(currentBank);
  
  // Send status message
  Serial.print("AD1 Activated - Switched to Bank ");
  Serial.println(currentBank + 1);
}

void turnOnBank(int bank) {
  if (bank < 0 || bank >= NUM_BANKS) return;
  
  // Send command to turn on all relays in the bank
  // ProXr uses 1-based bank numbering
  sendProXrCommand(RELAY_ON_ALL, bank + 1);
  
  // Update state tracking
  for (int relay = 0; relay < RELAYS_PER_BANK; relay++) {
    relayStates[bank][relay] = true;
  }
  
  Serial.print("Bank ");
  Serial.print(bank + 1);
  Serial.println(" - All Relays ON");
}

void turnOffBank(int bank) {
  if (bank < 0 || bank >= NUM_BANKS) return;
  
  // Send command to turn off all relays in the bank
  // ProXr uses 1-based bank numbering
  sendProXrCommand(RELAY_OFF_ALL, bank + 1);
  
  // Update state tracking
  for (int relay = 0; relay < RELAYS_PER_BANK; relay++) {
    relayStates[bank][relay] = false;
  }
  
  Serial.print("Bank ");
  Serial.print(bank + 1);
  Serial.println(" - All Relays OFF");
}

void turnOffAllRelays() {
  Serial.println("Turning off all relays...");
  for (int bank = 0; bank < NUM_BANKS; bank++) {
    turnOffBank(bank);
  }
}

void sendProXrCommand(byte command, byte data) {
  // NCD ProXr protocol: [PREFIX] [COMMAND] [DATA] [CHECKSUM]
  // Checksum = 255 - (sum of all bytes) + 1
  int sum = CMD_PREFIX + command + data;
  byte checksum = 255 - (sum & 0xFF) + 1;
  
  Serial.write(CMD_PREFIX);
  Serial.write(command);
  Serial.write(data);
  Serial.write(checksum);
  Serial.flush();
}

void turnOnRelay(int bank, int relay) {
  if (bank < 0 || bank >= NUM_BANKS) return;
  if (relay < 0 || relay >= RELAYS_PER_BANK) return;
  
  // Send command to turn on specific relay
  // ProXr uses 1-based relay numbering: relay 1-88
  byte relayNumber = (bank * RELAYS_PER_BANK) + relay + 1;
  sendProXrCommand(RELAY_ON, relayNumber);
  relayStates[bank][relay] = true;
}

void turnOffRelay(int bank, int relay) {
  if (bank < 0 || bank >= NUM_BANKS) return;
  if (relay < 0 || relay >= RELAYS_PER_BANK) return;
  
  // Send command to turn off specific relay
  // ProXr uses 1-based relay numbering: relay 1-88
  byte relayNumber = (bank * RELAYS_PER_BANK) + relay + 1;
  sendProXrCommand(RELAY_OFF, relayNumber);
  relayStates[bank][relay] = false;
}

void processSerialCommand() {
  // Read command from serial
  String command = Serial.readStringUntil('\n');
  command.trim();
  
  if (command.startsWith("BANK ")) {
    // Command format: BANK <number> ON/OFF
    int bankNum = command.substring(5, command.indexOf(' ', 5)).toInt() - 1;
    String action = command.substring(command.lastIndexOf(' ') + 1);
    
    if (bankNum >= 0 && bankNum < NUM_BANKS) {
      if (action == "ON") {
        turnOnBank(bankNum);
      } else if (action == "OFF") {
        turnOffBank(bankNum);
      }
    }
  } else if (command.startsWith("RELAY ")) {
    // Command format: RELAY <bank> <relay> ON/OFF
    int firstSpace = command.indexOf(' ');
    int secondSpace = command.indexOf(' ', firstSpace + 1);
    int thirdSpace = command.indexOf(' ', secondSpace + 1);
    
    int bankNum = command.substring(firstSpace + 1, secondSpace).toInt() - 1;
    int relayNum = command.substring(secondSpace + 1, thirdSpace).toInt() - 1;
    String action = command.substring(thirdSpace + 1);
    
    if (bankNum >= 0 && bankNum < NUM_BANKS && relayNum >= 0 && relayNum < RELAYS_PER_BANK) {
      if (action == "ON") {
        turnOnRelay(bankNum, relayNum);
      } else if (action == "OFF") {
        turnOffRelay(bankNum, relayNum);
      }
    }
  } else if (command == "STATUS") {
    printStatus();
  } else if (command == "ALL OFF") {
    turnOffAllRelays();
  } else if (command == "HELP") {
    printHelp();
  }
}

void printStatus() {
  Serial.println("\n=== Relay Controller Status ===");
  Serial.print("Current Active Bank: ");
  Serial.println(currentBank + 1);
  Serial.print("AD1 State: ");
  Serial.println(lastAD1State ? "HIGH" : "LOW");
  Serial.println("\nRelay States:");
  
  for (int bank = 0; bank < NUM_BANKS; bank++) {
    Serial.print("Bank ");
    Serial.print(bank + 1);
    Serial.print(": ");
    for (int relay = 0; relay < RELAYS_PER_BANK; relay++) {
      Serial.print(relayStates[bank][relay] ? "1" : "0");
    }
    Serial.println();
  }
  Serial.println("================================\n");
}

void printHelp() {
  Serial.println("\n=== NCD ProXr Relay Controller Commands ===");
  Serial.println("BANK <1-11> ON/OFF   - Turn all relays in a bank ON or OFF");
  Serial.println("RELAY <bank> <relay> ON/OFF - Turn specific relay ON or OFF");
  Serial.println("                       (bank: 1-11, relay: 1-8)");
  Serial.println("STATUS               - Display current relay states");
  Serial.println("ALL OFF              - Turn off all relays");
  Serial.println("HELP                 - Display this help message");
  Serial.println("\nAD1 Input: Automatically cycles through banks");
  Serial.println("==========================================\n");
}
