import os
import sys
import threading
import time
from scapy.all import sniff, IP, ICMP

BLOCKED_IPS = set()
lock = threading.Lock()

def packet_inspector(packet):
    if packet.haslayer(IP) and packet.haslayer(ICMP):
        src_ip = packet[IP].src

        # ICMP Type 8 is an Echo Request (Ping)
        if packet[ICMP].type == 8:
            with lock:
                if src_ip not in BLOCKED_IPS:
                    print(f"[!] Alert: Ping detected from {src_ip}")
                    trigger_firewall(src_ip)

def trigger_firewall(target_ip):
    print(f"FIREWALL TRIGGERED!: blocking {target_ip}")
    
    duration = 60
    cmd = f"sudo firewall-cmd --zone=FedoraWorkstation --add-rich-rule='rule family=\"ipv4\" source address=\"{target_ip}\" drop' --timeout={duration}"
    
    status = os.system(cmd)

    if status == 0:
        print(f"[✓] Successfully blocked {target_ip} for {duration} seconds.")
        BLOCKED_IPS.add(target_ip)
        
        # Start a timer thread to remove the IP from our memory set when the firewall rule expires
        threading.Thread(target=unblock_timer, args=(target_ip, duration), daemon=True).start()
    else:
        print(f"[✗] Failed to apply firewall rule for {target_ip}.")

def unblock_timer(target_ip, delay):
    time.sleep(delay)
    with lock:
        if target_ip in BLOCKED_IPS:
            BLOCKED_IPS.remove(target_ip)
            print(f"[*] Cooldown ended: {target_ip} removed from internal blocklist.")

if __name__ == "__main__":
    print("[*] Real-Time Packet Inspector Active. Listening for ICMP traffic...")
    try:
        sniff(filter="icmp", prn=packet_inspector, store=0)
    except KeyboardInterrupt:
        print("\n[*] Shutting down inspector.")
        sys.exit(0)