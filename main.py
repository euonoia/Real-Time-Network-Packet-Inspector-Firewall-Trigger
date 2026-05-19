import sys
from scapy.all import sniff
from detector import packet_inspector

if __name__ == "__main__":
    print("[*] Real-Time Packet Inspector Active. Listening for ICMP traffic...")
    try:
        sniff(filter="icmp", prn=packet_inspector, store=0)
    except KeyboardInterrupt:
        print("\n[*] Shutting down inspector.")
        sys.exit(0)