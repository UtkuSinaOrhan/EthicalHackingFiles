import subprocess   # runs code like run in terminal
import optparse     # provides the user to assign a value to a variable and can send an informational text
import re           # It is a library that allows the use of regular expressions. In this code, it is used to search for the MAC address.

def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i","--interface",dest="interface",help="interface to change!")
    parse_object.add_option("-m","--mac",dest="mac_address",help="new mac address")

    return parse_object.parse_args()

def change_mac_address(user_interface,user_mac_address):
    subprocess.call(["ifconfig",user_interface,"down"])
    subprocess.call(["ifconfig",user_interface,"hw","ether",user_mac_address])
    subprocess.call(["ifconfig",user_interface,"up"])

def control_new_mac(interface):
    ifconfig = subprocess.check_output(["ifconfig",interface])
    ifconfig = ifconfig.decode("utf-8")
    new_mac = re.search(r"(\w{2}:){5}\w{2}",ifconfig)

    if new_mac:
        return new_mac.group(0)
    else:
        return None



print("MyMacChanger started")
(user_input,arguments) = get_user_input()
change_mac_address(user_input.interface,user_input.mac_address)
finalized_mac = control_new_mac(user_input.interface)

if finalized_mac == user_input.mac_address:
    print("Success!")
else:
    print("Error!")