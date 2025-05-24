import scapy.all as scapy
import optparse


# 1) ARP  request
# 2) broadcast
# 3) response

def get_user_input():
    prs_obj = optparse.OptionParser()
    prs_obj.add_option("-i","--ipaddress",dest="ip_address",help="Enter IP Address")

    (user_input,arguments) = prs_obj.parse_args()

    if not user_input.ip_address:
        print("Enter IP Address")

    return user_input


def scan_my_network(ip):

    arp_request_packet = scapy.ARP(pdst=ip)
    #scapy.ls(scapy.ARP())
    broadcast_packet = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    #scapy.ls(scapy.Ether())
    combined_packet = broadcast_packet/arp_request_packet
    (answer_list,unanswered_list) = scapy.srp(combined_packet,timeout = 1)
    answer_list.summary()


user_ip_address = get_user_input()
scan_my_network(user_ip_address.ip_address)