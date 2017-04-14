#! /bin/bash
#allows remote connections to local host. sec risk, but not a big deal as little process 
#exposed anyways
echo 0 > /proc/sys/net/ipv4/conf/wlp3s0/route_localnet

#allows ip forwarding. yay, now a router
echo 0 > /proc/sys/net/ipv4/ip_forward

iptables-restore < old
