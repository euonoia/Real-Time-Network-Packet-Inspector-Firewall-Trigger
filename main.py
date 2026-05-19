from scapy.all import sniff
from src.inspector import packet_inspector

def main():
    print("[*] Starting IPS Sniffer... Press Ctrl+C to stop.")
    # Sniff network traffic and pass it to our inspector module
    sniff(prn=packet_inspector, store=0)

if __name__ == "__main__":
    main()