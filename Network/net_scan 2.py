#! /usr/bin/env python3



import scapy.all as scapy
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", default = "eth0" ,dest="interface", help="Interface to change mac")
    parser.add_argument("-r", "--range", dest="range", help="IP or range of IP")
    options = parser.parse_args()
    if not options.range:
        parser.error("Specify a range or IP address, use --help for info")
    return options

def scan(ip,interface):
    #scapy.arping(ip)

    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_r_b = broadcast/arp_request
    ans = scapy.srp(arp_r_b,timeout=10,iface = interface,verbose=False)[0]
    #print(ans.summary())

    clients_list=[]
    
    for element in ans:
        client_dict = {"ip":element[1].psrc, "mac":element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_net(c_list):
     print("IP\t\t\t","Mac_Address")
     print("---------------------------------------")
     for i in c_list:
         print(i["ip"],"\t\t",i["mac"])

options = get_args()
c = scan(options.range,options.interface)
print_net(c)
