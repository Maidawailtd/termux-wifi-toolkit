# 🛰️ Ultimate Termux WiFi Toolkit

![Termux WiFi Toolkit Banner](https://i.imgur.com/JQm6z7K.png)

Advanced WiFi analysis and security toolkit for Termux with wardriving capabilities. Created by **Shafiu Shehu (MGLINK)**.

[![Telegram](https://img.shields.io/badge/Telegram-@mglinkco-blue.svg)](https://t.me/mglinkco)
![Version](https://img.shields.io/badge/Version-2.1-green.svg)

## 📌 Legal Disclaimer
> **⚠️ WARNING:** This tool is for **educational purposes only**. Unauthorized network scanning/access is illegal. You must have explicit permission from network owners. The creator assumes no liability for misuse.

## 🌟 Features
- 📡 WiFi network scanning and analysis
- 🚗 Wardriving with GPS logging
- 🔍 Security vulnerability detection
- 🛡️ MAC address tools (block/allow/spoof)
- 📊 Signal strength visualization
- 📁 Database storage for scan results
- 🎨 Color-coded terminal interface

## 📥 Installation
```bash
# 1. Install dependencies
pkg update && pkg install -y git python nmap sqlite

# 2. Clone repository
git clone https://github.com/Maidawailtd/termux-wifi-toolkit.git
cd termux-wifi-toolkit

# 3. Make executable
chmod +x wifi_toolkit.py

# 4. Run the toolkit
./wifi_toolkit.py

/sdcard/wifi_toolkit/
├── networks.db         # SQLite database
├── wardrive.log        # GPS-logged scans
└── requirements.txt    # Python dependencies
