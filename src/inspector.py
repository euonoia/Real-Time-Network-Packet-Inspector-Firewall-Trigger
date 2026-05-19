from scapy.all import IP, ICMP
from src.config import BLOCKED_IPS, lock
from src.firewall import trigger_firewall

def packet_inspector(packet):
    if packet.haslayer(IP) and packet.haslayer(ICMP):
        src_ip = packet[IP].src

        # ICMP Type 8 is an Echo Request (Ping)
        if packet[ICMP].type == 8:
            with lock:
                is_blocked = src_ip in BLOCKED_IPS
            
            if not is_blocked:
                print(f"[!] Alert: Ping detected from {src_ip}")
                trigger_firewall(src_ip)