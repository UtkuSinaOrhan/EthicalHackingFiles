import subprocess   # Allows the execution of system commands (e.g., like using the terminal)
import optparse     # Used to parse command-line options and arguments
import re           # Regular expression module, used here for extracting the MAC address

# Function to get user input from command-line arguments
def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i", "--interface", dest="interface", help="Interface to change the MAC address for")
    parse_object.add_option("-m", "--mac", dest="mac_address", help="New MAC address to assign")

    return parse_object.parse_args()  # Returns parsed user input

# Function to change the MAC address of a given network interface
def change_mac_address(user_interface, user_mac_address):
    subprocess.call(["ifconfig", user_interface, "down"])                     # Disable the network interface
    subprocess.call(["ifconfig", user_interface, "hw", "ether", user_mac_address])  # Change the MAC address
    subprocess.call(["ifconfig", user_interface, "up"])                       # Re-enable the network interface

# Function to check the current MAC address of the interface after the change
def control_new_mac(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface])  # Run 'ifconfig' and get output
    ifconfig = ifconfig.decode("utf-8")                           # Decode bytes to string
    new_mac = re.search(r"(\w{2}:){5}\w{2}", ifconfig)           # Search for MAC address pattern using regex

    if new_mac:
        return new_mac.group(0)  # Return the matched MAC address
    else:
        return None  # If no MAC address found, return None


# Main program logic
print("MyMacChanger started")
(user_input, arguments) = get_user_input()  # Get user-provided interface and MAC address
change_mac_address(user_input.interface, user_input.mac_address)  # Attempt to change MAC
finalized_mac = control_new_mac(user_input.interface)  # Get current MAC to verify change

# Compare the MAC address after change with the user input
if finalized_mac == user_input.mac_address:
    print("Success!")  # MAC address changed successfully
else:
    print("Error!")    # MAC address change failed
