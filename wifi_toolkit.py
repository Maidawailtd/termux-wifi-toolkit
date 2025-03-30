#!/data/data/com.termux/files/usr/bin/python3
import os
import sys
import json
import time
import sqlite3
import subprocess
from datetime import datetime

# Color codes for terminal
COLORS = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'purple': '\033[95m',
    'cyan': '\033[96m',
    'end': '\033[0m'
}

# Tool Information
TOOL_INFO = f"""
{COLORS['purple]}
╔══════════════════════════════════════════════╗
║            ULTIMATE WIFI TOOLKIT             ║
╠══════════════════════════════════════════════╣
║ Version: 2.1                                 ║
║ Created by: Shafiu Shehu (MGLINK)            ║
║ Telegram: @mglinkco                          ║
║                                              ║
║ LEGAL NOTICE:                                ║
║ For educational purposes only.               ║
║ Unauthorized access is prohibited.           ║
╚══════════════════════════════════════════════╝
{COLORS['end']}
"""

class UltimateWiFiToolkit:
    def __init__(self):
        self.show_creator_info()
        self.check_requirements()
        self.setup_environment()
        self.init_db()
        
    def show_creator_info(self):
        """Display creator information on startup"""
        os.system('clear')
        print(TOOL_INFO)
        time.sleep(2)  # Pause for visibility

    def color_print(self, text, color='green'):
        print(f"{COLORS.get(color, '')}{text}{COLORS['end']}")

    def check_requirements(self):
        requirements = {
            'python': 'python --version',
            'nmap': 'nmap --version',
            'sqlite3': 'sqlite3 --version'
        }
        
        missing = []
        self.color_print("\n🔍 Checking requirements...", 'blue')
        
        for pkg, cmd in requirements.items():
            try:
                subprocess.check_call(cmd, shell=True, 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
                self.color_print(f"✅ {pkg.ljust(10)} - Installed", 'green')
            except:
                missing.append(pkg)
                self.color_print(f"❌ {pkg.ljust(10)} - Missing", 'red')
        
        if missing:
            self.color_print("\n⚙️ Installing missing packages...", 'yellow')
            subprocess.call(f"pkg install -y {' '.join(missing)}", shell=True)

    def setup_environment(self):
        self.data_dir = "/sdcard/wifi_toolkit"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Create requirements.txt if not exists
        req_file = os.path.join(self.data_dir, "requirements.txt")
        if not os.path.exists(req_file):
            with open(req_file, 'w') as f:
                f.write("python-nmap\nmatplotlib\nscapy\ngps3")

    def init_db(self):
        self.db_file = os.path.join(self.data_dir, "networks.db")
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS networks
                    (id INTEGER PRIMARY KEY,
                    ssid TEXT, bssid TEXT, 
                    security TEXT, channel INTEGER,
                    lat REAL, lon REAL,
                    timestamp DATETIME, rssi INTEGER)''')
        conn.commit()
        conn.close()

    def show_menu(self):
        os.system('clear')
        self.color_print("\n" + "="*50, 'blue')
        self.color_print("🛰️ ULTIMATE TERMUX WIFI TOOLKIT", 'yellow')
        self.color_print("="*50, 'blue')
        print("\n1. Scan Nearby Networks")
        print("2. Current Connection Info")
        print("3. Wardriving Mode")
        print("4. Security Analysis")
        print("5. MAC Address Tools")
        print("6. Install Python Packages")
        print("0. Exit\n")
        
        try:
            return input("Select an option (0-6): ")
        except KeyboardInterrupt:
            self.clean_exit()

    def run_tool(self, choice):
        tools = {
            '1': self.scan_networks,
            '2': self.connection_info,
            '3': self.wardrive,
            '4': self.security_scan,
            '5': self.mac_tools,
            '6': self.install_python_pkgs
        }
        tools.get(choice, self.invalid_option)()

    def scan_networks(self):
        self.color_print("\n📡 Scanning networks...", 'yellow')
        try:
            result = subprocess.check_output("termux-wifi-scaninfo", shell=True)
            networks = json.loads(result)
            
            self.color_print("\nFound Networks:", 'blue')
            for i, net in enumerate(networks, 1):
                print(f"{i}. {net['ssid']} ({net['rssi']}dBm) - {net['bssid']}")
                
            self.save_to_db(networks)
        except Exception as e:
            self.color_print(f"Error: {str(e)}", 'red')

    def connection_info(self):
        self.color_print("\n📶 Current Connection:", 'blue')
        try:
            info = json.loads(subprocess.check_output("termux-wifi-connectioninfo", shell=True))
            print(f"SSID: {info.get('ssid', 'Unknown')}")
            print(f"IP: {info.get('ip', 'N/A')}")
            print(f"Signal: {info.get('rssi', 0)} dBm")
            print(f"MAC: {info.get('mac_address', 'Unknown')}")
        except Exception as e:
            self.color_print(f"Error: {str(e)}", 'red')

    def wardrive(self):
        self.color_print("\n🚗 Starting Wardrive Mode (Ctrl+C to stop)...", 'yellow')
        try:
            while True:
                nets = json.loads(subprocess.check_output("termux-wifi-scaninfo", shell=True))
                loc = json.loads(subprocess.check_output("termux-location", shell=True))
                
                with open(os.path.join(self.data_dir, "wardrive.log"), 'a') as f:
                    for net in nets:
                        log_entry = (f"{datetime.now()},{net['ssid']},{net['bssid']},"
                                   f"{loc.get('latitude','N/A')},{loc.get('longitude','N/A')},"
                                   f"{net['rssi']}\n")
                        f.write(log_entry)
                
                self.color_print(f"📍 {loc.get('latitude','N/A')},{loc.get('longitude','N/A')} | 📡 {len(nets)} networks", 'green')
                time.sleep(10)
        except KeyboardInterrupt:
            self.color_print("\n📁 Data saved to wardrive.log", 'blue')

    def security_scan(self):
        self.color_print("\n🔒 Running Security Analysis...", 'yellow')
        try:
            # WPS vulnerability check
            self.color_print("\nWPS Status:", 'blue')
            os.system("wash -i wlan0 2>&1 | head -n 5 || echo 'Install Reaver first'")
            
            # Encryption check
            self.color_print("\nEncryption Analysis:", 'blue')
            os.system("termux-wifi-connectioninfo | grep -i 'WPA\\|WEP\\|WPA2'")
        except Exception as e:
            self.color_print(f"Error: {str(e)}", 'red')

    def mac_tools(self):
        self.color_print("\n🛡️ MAC Address Tools:", 'blue')
        print("1. Block MAC Address")
        print("2. Allow MAC Address")
        print("3. Spoof MAC Address")
        choice = input("Select: ")
        
        if choice == '1':
            mac = input("Enter MAC to block: ")
            os.system(f"iptables -A INPUT -m mac --mac-source {mac} -j DROP")
            self.color_print(f"Blocked {mac}", 'green')
        elif choice == '2':
            mac = input("Enter MAC to allow: ")
            os.system(f"iptables -D INPUT -m mac --mac-source {mac} -j DROP")
            self.color_print(f"Allowed {mac}", 'green')
        elif choice == '3':
            self.color_print("⚠️ Requires root access!", 'red')
            interface = input("Interface (wlan0): ") or "wlan0"
            os.system(f"su -c 'ifconfig {interface} down && macchanger -r {interface} && ifconfig {interface} up'")

    def install_python_pkgs(self):
        self.color_print("\n📦 Installing Python packages...", 'yellow')
        os.system("pip install -r /sdcard/wifi_toolkit/requirements.txt")

    def save_to_db(self, networks):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        for net in networks:
            c.execute('''INSERT INTO networks 
                        (ssid, bssid, timestamp, rssi)
                        VALUES (?,?,?,?)''',
                     (net['ssid'], net['bssid'], datetime.now(), net['rssi']))
        conn.commit()
        conn.close()
        self.color_print(f"💾 Saved {len(networks)} networks to database", 'green')

    def invalid_option(self):
        self.color_print("Invalid option!", 'red')
        time.sleep(1)

    def clean_exit(self):
        self.color_print("\n🛑 Exiting toolkit...", 'red')
        sys.exit(0)

    def main(self):
        while True:
            choice = self.show_menu()
            if choice == '0':
                self.clean_exit()
            else:
                self.run_tool(choice)
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    tool = UltimateWiFiToolkit()
    tool.main()
