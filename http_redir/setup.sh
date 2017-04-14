#! /bin/bash

iptables-save > old

#allows remote connections to local host. sec risk, but not a big deal as little process 
#exposed anyways
echo 1 > /proc/sys/net/ipv4/conf/wlp3s0/route_localnet

#allows ip forwarding. yay, now a router
echo 1 > /proc/sys/net/ipv4/ip_forward

#redirect traffic on wlp3s0 from 80 to 1337
iptables -t nat -A PREROUTING -i wlp3s0 -p tcp --dport 80 -j REDIRECT --to-port 1337

#accept input on wlp3s0
iptables -A INPUT -i wlp3s0 -j ACCEPT

#forward on wlp3s0
iptables -A FORWARD -i wlp3s0 -j ACCEPT
