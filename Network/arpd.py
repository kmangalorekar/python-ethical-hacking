
import scapy.all as scapy

def sniff(interface):
    scapy.sniff(iface=interface, store = False, prn = p_s_p)


def get_mac(ip):
    #scapy.arping(ip)
    
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_r_b = broadcast/arp_request
    ans = scapy.srp(arp_r_b,timeout=1,verbose=False)[0]
    #print(ans.summary())
    return ans[0][1].hwsrc

def p_s_p(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op==2:
	try:		
		real_mac = get_mac(packet[scapy.ARP].psrc)
		response_mac = packet[scapy.ARP].hwsrc
		if real_mac != response_mac:
		    print "Unter attack!!"
	except IndexError:
		pass        
	#print(packet.show())
        




try:
    sniff("wlan0")
    raise KeyboardInterrupt("keyboard interruption")
except KeyboardInterrupt:
    print "Detected Ctrl+C,exiting"
