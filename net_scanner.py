import scapy.all as scapy
import optparse

# 1) ARP request
# 2) Broadcast
# 3) Response handling

# Function to get IP address input from the user via command line
def get_user_input():
    prs_obj = optparse.OptionParser()  # Create an option parser object
    prs_obj.add_option("-i", "--ipaddress", dest="ip_address", help="Enter IP Address")  # Add an IP address option

    (user_input, arguments) = prs_obj.parse_args()  # Parse the command-line arguments

    if not user_input.ip_address:  # If the user did not provide an IP address
        print("Enter IP Address")

    return user_input  # Return the parsed user input object

# Function to scan the network for active devices
def scan_my_network(ip):
    # Create an ARP request packet with the provided IP address or IP range
    arp_request_packet = scapy.ARP(pdst=ip)

    # Create an Ethernet frame with a broadcast destination MAC address
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    # Combine the Ethernet frame and the ARP request into one packet
    combined_packet = broadcast_packet / arp_request_packet

    # Send the packet on the network and wait for responses
    # srp() sends and receives packets at layer 2 (Ethernet)
    (answer_list, unanswered_list) = scapy.srp(combined_packet, timeout=1, verbose=False)

    # Display a summary of received responses
    answer_list.summary()

# Get the user-provided IP address from command line arguments
user_ip_address = get_user_input()

# Start scanning the network using the provided IP address
scan_my_network(user_ip_address.ip_address)
