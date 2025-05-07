import subprocess 
import optparse
import re 

def get_arguments():
    parser = optparse.OptionParser()
    # Improved help messages with examples
    parser.add_option('-i', dest="interface", 
                    help="Network interface (e.g., eth0, wlan0)")
    parser.add_option('-m', dest="new_mac",
                    help="New MAC address (e.g., 00:11:22:33:44:55)")
    options, arguments = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface. Use -h for help.")
    if not options.new_mac:
        parser.error("[-] Please specify a MAC address. Use -h for help.")
    return options

def mac_changer(interface, new_mac):
    try:
        # Use check_call to ensure commands succeed
        subprocess.check_call(f"ifconfig {interface} down", shell=True)
        subprocess.check_call(f"ifconfig {interface} hw ether {new_mac}", shell=True)
        subprocess.check_call(f"ifconfig {interface} up", shell=True)
        print(f"[+] Changed MAC address for {interface} to {new_mac}")
    except subprocess.CalledProcessError as e:
        print(f"[-] Command failed: {e}")
        exit(1)

def get_current_mac(interface):
    try:
        ifconfig_result = subprocess.check_output(
            f"ifconfig {interface}", 
            shell=True, 
            stderr=subprocess.DEVNULL  # Hide error messages
        ).decode()
    except subprocess.CalledProcessError:
        return None
    
    # Improved regex for MAC address matching
    mac_match = re.search(r"([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}", ifconfig_result)
    return mac_match.group(0) if mac_match else None

options = get_arguments()

# Store original MAC before changing
original_mac = get_current_mac(options.interface)
print(f"[*] Original MAC: {original_mac or 'Not found'}")

# Change MAC address
mac_changer(options.interface, options.new_mac)

# Verify change
current_mac = get_current_mac(options.interface)

if not current_mac:
    print("[-] Failed to retrieve MAC address after change")
elif current_mac.lower() == options.new_mac.lower():
    print(f"[+] MAC address successfully changed to {current_mac}")
else:
    print(f"[-] MAC change failed. Current MAC: {current_mac}")