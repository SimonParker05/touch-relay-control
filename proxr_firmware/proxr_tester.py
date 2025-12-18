#!/usr/bin/env python3
"""
NCD ProXr Relay Controller Tester

This script provides a command-line interface to test and control
the NCD ProXr relay controller via USB serial connection.
"""

import serial
import time
import sys
import argparse

class ProXrController:
    """Interface to NCD ProXr Relay Controller"""
    
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        """Initialize serial connection to ProXr controller"""
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset
            print(f"Connected to {port} at {baudrate} baud")
            self._read_startup_messages()
        except serial.SerialException as e:
            print(f"Error: Could not open serial port {port}")
            print(f"Details: {e}")
            sys.exit(1)
    
    def _read_startup_messages(self):
        """Read and display startup messages from controller"""
        time.sleep(0.5)
        while self.ser.in_waiting:
            line = self.ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"Controller: {line}")
    
    def send_command(self, command):
        """Send a command to the controller and read response"""
        self.ser.write(f"{command}\n".encode())
        time.sleep(0.2)
        
        response = []
        while self.ser.in_waiting:
            line = self.ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                response.append(line)
                print(line)
        
        return response
    
    def turn_on_bank(self, bank):
        """Turn on all relays in a bank (1-11)"""
        print(f"\nTurning ON Bank {bank}...")
        return self.send_command(f"BANK {bank} ON")
    
    def turn_off_bank(self, bank):
        """Turn off all relays in a bank (1-11)"""
        print(f"\nTurning OFF Bank {bank}...")
        return self.send_command(f"BANK {bank} OFF")
    
    def turn_on_relay(self, bank, relay):
        """Turn on a specific relay (bank: 1-11, relay: 1-8)"""
        print(f"\nTurning ON Relay {relay} in Bank {bank}...")
        return self.send_command(f"RELAY {bank} {relay} ON")
    
    def turn_off_relay(self, bank, relay):
        """Turn off a specific relay (bank: 1-11, relay: 1-8)"""
        print(f"\nTurning OFF Relay {relay} in Bank {bank}...")
        return self.send_command(f"RELAY {bank} {relay} OFF")
    
    def get_status(self):
        """Get current status of all relays"""
        print("\nGetting status...")
        return self.send_command("STATUS")
    
    def turn_off_all(self):
        """Turn off all relays"""
        print("\nTurning OFF all relays...")
        return self.send_command("ALL OFF")
    
    def show_help(self):
        """Display controller help"""
        print("\nGetting help from controller...")
        return self.send_command("HELP")
    
    def interactive_mode(self):
        """Start interactive command mode"""
        print("\n=== Interactive Mode ===")
        print("Enter commands or type 'exit' to quit")
        print("Type 'help' for available commands\n")
        
        while True:
            try:
                cmd = input("ProXr> ").strip()
                
                if cmd.lower() == 'exit' or cmd.lower() == 'quit':
                    print("Exiting...")
                    break
                elif cmd.lower() == 'help':
                    self.show_local_help()
                elif cmd:
                    self.send_command(cmd)
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def show_local_help(self):
        """Display local help for this tester script"""
        print("\n=== ProXr Tester Commands ===")
        print("Controller Commands:")
        print("  BANK <1-11> ON/OFF          - Turn bank on/off")
        print("  RELAY <bank> <relay> ON/OFF - Turn specific relay on/off")
        print("  STATUS                      - Show relay states")
        print("  ALL OFF                     - Turn off all relays")
        print("  HELP                        - Show controller help")
        print("\nTester Commands:")
        print("  help                        - Show this help")
        print("  exit/quit                   - Exit interactive mode")
        print("=============================\n")
    
    def test_sequence(self):
        """Run a test sequence through all banks"""
        print("\n=== Running Test Sequence ===")
        print("This will cycle through all 11 banks")
        
        # Turn off all relays first
        self.turn_off_all()
        time.sleep(1)
        
        # Cycle through each bank
        for bank in range(1, 12):
            print(f"\n--- Testing Bank {bank} ---")
            self.turn_on_bank(bank)
            time.sleep(2)
            self.turn_off_bank(bank)
            time.sleep(1)
        
        print("\n=== Test Sequence Complete ===")
    
    def close(self):
        """Close serial connection"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial connection closed")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='NCD ProXr Relay Controller Tester',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (default)
  python proxr_tester.py
  
  # Specify custom port
  python proxr_tester.py -p /dev/ttyACM0
  
  # Run test sequence
  python proxr_tester.py --test
  
  # Get status
  python proxr_tester.py --status
  
  # Turn on bank 1
  python proxr_tester.py --bank 1 --on
  
  # Turn on relay 5 in bank 3
  python proxr_tester.py --relay 3 5 --on
        """
    )
    
    parser.add_argument('-p', '--port', 
                        default='/dev/ttyUSB0',
                        help='Serial port (default: /dev/ttyUSB0)')
    parser.add_argument('-b', '--baudrate',
                        type=int,
                        default=115200,
                        help='Baud rate (default: 115200)')
    parser.add_argument('--test',
                        action='store_true',
                        help='Run test sequence through all banks')
    parser.add_argument('--status',
                        action='store_true',
                        help='Get current status')
    parser.add_argument('--bank',
                        type=int,
                        metavar='N',
                        help='Bank number (1-11)')
    parser.add_argument('--relay',
                        nargs=2,
                        type=int,
                        metavar=('BANK', 'RELAY'),
                        help='Relay bank and number (1-11, 1-8)')
    parser.add_argument('--on',
                        action='store_true',
                        help='Turn on (use with --bank or --relay)')
    parser.add_argument('--off',
                        action='store_true',
                        help='Turn off (use with --bank or --relay)')
    parser.add_argument('--all-off',
                        action='store_true',
                        help='Turn off all relays')
    
    args = parser.parse_args()
    
    # Validate argument combinations before connecting
    if args.bank:
        if not (args.on or args.off):
            print("Error: Specify --on or --off with --bank")
            sys.exit(1)
        if args.on and args.off:
            print("Error: Cannot specify both --on and --off")
            sys.exit(1)
        if args.bank < 1 or args.bank > 11:
            print("Error: Bank number must be 1-11")
            sys.exit(1)
    
    if args.relay:
        if not (args.on or args.off):
            print("Error: Specify --on or --off with --relay")
            sys.exit(1)
        if args.on and args.off:
            print("Error: Cannot specify both --on and --off")
            sys.exit(1)
        bank, relay = args.relay
        if bank < 1 or bank > 11:
            print("Error: Bank number must be 1-11")
            sys.exit(1)
        if relay < 1 or relay > 8:
            print("Error: Relay number must be 1-8")
            sys.exit(1)
    
    # Create controller instance
    controller = ProXrController(args.port, args.baudrate)
    
    try:
        # Execute requested action
        if args.test:
            controller.test_sequence()
        elif args.status:
            controller.get_status()
        elif args.all_off:
            controller.turn_off_all()
        elif args.bank:
            if args.on:
                controller.turn_on_bank(args.bank)
            else:
                controller.turn_off_bank(args.bank)
        elif args.relay:
            bank, relay = args.relay
            if args.on:
                controller.turn_on_relay(bank, relay)
            else:
                controller.turn_off_relay(bank, relay)
        else:
            # Default to interactive mode
            controller.interactive_mode()
    
    finally:
        controller.close()

if __name__ == '__main__':
    main()
