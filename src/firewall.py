import os
import time
import threading
from src.config import BLOCKED_IPS, lock

def trigger_firewall(target_ip):
    print(f"FIREWALL TRIGGERED!: blocking {target_ip}")
    
    duration = 60
    cmd = f"sudo firewall-cmd --zone=FedoraWorkstation --add-rich-rule='rule family=\"ipv4\" source address=\"{target_ip}\" drop' --timeout={duration}"
    
    status = os.system(cmd)

    if status == 0:
        print(f"[✓] Successfully blocked {target_ip} for {duration} seconds.")
        with lock:
            BLOCKED_IPS.add(target_ip)
        
        # Start the cooldown timer
        threading.Thread(target=_unblock_timer, args=(target_ip, duration), daemon=True).start()
    else:
        print(f"[✗] Failed to apply firewall rule for {target_ip}.")

def _unblock_timer(target_ip, delay):
    """Prefixed with an underscore because it's an internal helper function"""
    time.sleep(delay)
    with lock:
        if target_ip in BLOCKED_IPS:
            BLOCKED_IPS.remove(target_ip)
            print(f"[*] Cooldown ended: {target_ip} removed from internal blocklist.")