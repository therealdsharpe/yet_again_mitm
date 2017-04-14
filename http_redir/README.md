# yet_another_mitm
mitm script using scapy. nothing special


run setup.sh as root to setup iptables (dw, it saves the old config)
run arp_spoofer.py to arp poising victim computer
in another window, run roller.py as normal user.

unconfigured, runs in maymay mode

requires a folder called maymays, filled with webm files.
these videos will then be viewed whenever the person looks at a http webpage
