#! /usr/bin/env python

import subprocess
import optparse
import re



def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change mac")
    parser.add_option("-m", "--mac", dest="new_mac", help="New mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Specify a interface, use --help for info")

    elif not options.new_mac:
        parser.error("Specify a mac, use --help for info")
    return options


def change_mac(interface,new_mac):
    print("[+] Changing value for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_mac(interface,new_mac):
    if_res = subprocess.check_output(["ifconfig",interface])
    #print(if_res.decode('utf-8'))

    eth = re.search("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(if_res))

    if eth:
        return eth.group(0)

    else:
        print("could not read mac address")

def check_mac (current_mac,new_mac):
    if current_mac == new_mac:
        print("[+]New mac changed to : " + str(current_mac))
    else:
        print('Mac not changed')

options = get_args()

change_mac(options.interface,options.new_mac)

current_mac = get_mac(options.interface,options.new_mac)

if current_mac:
    check_mac(current_mac,options.new_mac)