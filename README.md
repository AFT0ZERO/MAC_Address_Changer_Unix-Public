# MAC Address Changer

A Python script to securely change MAC addresses on Linux systems.

## 📥 Installation
```bash
git clone https://github.com/yourusername/mac-changer.git
cd mac-changer
sudo chmod +x mac_changer.py
```

## 🚀 Usage
```bash
sudo ./mac_changer.py -i [interface] -m [new_mac]
```

## Example
```bash
sudo ./mac_changer.py -i eth0 -m 00:11:22:33:44:55
```

## 📝 Requirements
- Python 3.6+
- Linux OS
- Root privileges
- `ifconfig` utility

## ⚠ Legal Notice
Use only on networks where you have explicit permission.
