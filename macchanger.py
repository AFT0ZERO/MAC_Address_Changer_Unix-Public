import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', dest="interface",
                      help="Network interface (e.g., eth0, wlan0)")
    parser.add_option('-m', dest="new_mac",
                      help="New MAC address (e.g., 00:11:22:33:44:55)")
    options, _ = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface. Use -h for help.")
    if not options.new_mac:
        parser.error("[-] Please specify a MAC address. Use -h for help.")
    
    return options

def mac_changer(interface, new_mac):
    commands = [
        ['ifconfig', interface, 'down'],
        ['ifconfig', interface, 'hw', 'ether', new_mac],
        ['ifconfig', interface, 'up']
    ]
    
    try:
        for cmd in commands:
            subprocess.check_call(cmd)
        print(f"[+] Changed MAC address for {interface} to {new_mac}")
    except subprocess.CalledProcessError as e:
        print(f"[-] Command failed: {' '.join(e.cmd)}")
        print(f"    Error: {e}")
        exit(1)

def get_current_mac(interface):
    try:
        output = subprocess.check_output(
            ['ifconfig', interface],
            stderr=subprocess.DEVNULL
        ).decode()
    except subprocess.CalledProcessError:
        return None
    
    mac_match = re.search(r"([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}", output)
    return mac_match.group(0) if mac_match else None

def main():
    options = get_arguments()
    
    # Validate MAC format before making changes
    if not re.match(r"^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$", options.new_mac):
        print(f"[-] Invalid MAC address format: {options.new_mac}")
        exit(1)
    
    original_mac = get_current_mac(options.interface)
    if original_mac:
        print(f"[*] Original MAC: {original_mac}")
    else:
        print(f"[-] Could not determine current MAC for {options.interface}")
    
    mac_changer(options.interface, options.new_mac)
    
    current_mac = get_current_mac(options.interface)
    if not current_mac:
        print("[-] Failed to verify MAC address after change")
        exit(1)
    
    if current_mac.lower() == options.new_mac.lower():
        print(f"[+] Success! MAC address changed to {current_mac}")
    else:
        print(f"[-] MAC change failed. Current MAC: {current_mac}")
        exit(1)

if __name__ == "__main__":
    main()