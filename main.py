from scapy.all import sniff
from src.inspector import packet_inspector

def main():
    print("[*] Real Time Network Packet Inspector Firewall Press Ctrl+C to stop.")
    sniff(prn=packet_inspector, store=0)

if __name__ == "__main__":
    main()