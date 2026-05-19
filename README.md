# Scapy ICMP Packet Inspector (v1)

## Overview

This project is a real-time ICMP packet inspector written in Python
using Scapy.\
The script listens for incoming ICMP Echo Request packets (ping
requests) and automatically triggers a firewall rule to temporarily
block the detected source IP address.

The goal of this implementation is to provide a simple intrusion
detection and automated response mechanism against repeated ICMP
traffic.

------------------------------------------------------------------------

## Features

-   Real-time packet inspection using Scapy
-   Detects ICMP Echo Request packets (Ping)
-   Automatically applies firewall blocking rules
-   Temporary blocking using firewall timeout
-   Uses multithreading for cooldown handling
-   Prevents duplicate blocking using an internal memory set

------------------------------------------------------------------------

## Technologies Used

-   Python 3
-   Scapy
-   threading
-   os
-   sys
-   firewalld (firewall-cmd)

------------------------------------------------------------------------

## Project Workflow

1.  Program starts and begins listening for ICMP traffic.
2.  Scapy captures packets.
3.  Packet is checked:
    -   Must contain an IP layer
    -   Must contain an ICMP layer
4.  If packet type equals `8`:
    -   Type `8` represents an ICMP Echo Request (Ping)
5.  Source IP is extracted.
6.  Firewall rule is created dynamically.
7.  IP is blocked for 60 seconds.
8.  Timer thread removes the IP from the internal blocklist after
    expiration.

------------------------------------------------------------------------

## Code Components

### Global Variables

`BLOCKED_IPS` - Stores blocked IP addresses - Prevents repeated firewall
commands

`lock` - Thread lock used for synchronization - Prevents race conditions

------------------------------------------------------------------------

### Functions

#### packet_inspector(packet)

Purpose: - Inspects captured packets - Checks whether packet is an ICMP
Echo Request

Process: - Verify IP layer exists - Verify ICMP layer exists - Extract
source IP - Detect ICMP Type 8 - Trigger firewall action

------------------------------------------------------------------------

#### trigger_firewall(target_ip)

Purpose: - Dynamically creates a firewall rule

Process: - Builds firewall-cmd command - Applies temporary block for 60
seconds - Adds IP into `BLOCKED_IPS` - Starts cooldown timer thread

Firewall command:

``` bash
sudo firewall-cmd --zone=FedoraWorkstation --add-rich-rule='rule family="ipv4" source address="TARGET_IP" drop' --timeout=60
```

------------------------------------------------------------------------

#### unblock_timer(target_ip, delay)

Purpose: - Removes IP from memory after firewall timeout expires

Process: - Waits for delay period - Removes IP from internal set

------------------------------------------------------------------------

## Commands Used During Setup

### Get Local IP Address

``` bash
ip route get 1 | awk '{print $7; exit}'
```

Purpose: - Retrieves the local IP address of the machine

------------------------------------------------------------------------

### Get Active Firewall Zone

``` bash
sudo firewall-cmd --get-active-zones
```

Purpose: - Displays active firewalld zones

Example output:

``` bash
FedoraWorkstation
  interfaces: wlp0s20f3
```
------------------------------------------------------------------------
### Run the Setup

# 1. Create a virtual environment
python3 -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate

# 3. Install the requirements
pip install -r requirements.txt

------------------------------------------------------------------------

### Run the Program

``` bash
sudo ./venv/bin/python inspector.py
```

Purpose: - Runs the packet inspector with elevated privileges - Root
permissions are required for packet sniffing and firewall modifications

------------------------------------------------------------------------

## Sample Program Output

``` text
[*] Real-Time Packet Inspector Active. Listening for ICMP traffic...

[!] Alert: Ping detected from 192.168.1.15

FIREWALL TRIGGERED!: blocking 192.168.1.15

[✓] Successfully blocked 192.168.1.15 for 60 seconds.

[*] Cooldown ended: 192.168.1.15 removed from internal blocklist.
```

------------------------------------------------------------------------

## Notes

-   Scapy requires elevated permissions for packet sniffing.
-   firewalld must be installed and running.
-   The firewall zone name may vary depending on system configuration.
-   This implementation currently handles only ICMP Echo Requests.
-   IPv6 traffic is not yet supported.


