import threading

# Shared thread-safe state
BLOCKED_IPS = set()
lock = threading.Lock()