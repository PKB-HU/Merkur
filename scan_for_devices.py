# scanner.py

import socket
import ipaddress
import concurrent.futures
import json
import threading
import time
import comms

PORT_TO_SCAN = 6274
TIMEOUT = 1  # seconds
OUTPUT_FILE = "devices.json"
SCAN_INTERVAL = 30  # seconds

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def scan_port(ip):
    try:
        with socket.create_connection((ip, PORT_TO_SCAN), timeout=TIMEOUT):
            return ip
    except (socket.timeout, ConnectionRefusedError, OSError):
        return None

def scan_network():
    local_ip = get_local_ip()
    subnet = ipaddress.ip_network(local_ip + '/24', strict=False)

    found = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, str(ip)): ip for ip in subnet.hosts()}
        for future in concurrent.futures.as_completed(futures):
            ip = futures[future]
            result = future.result()
            if result:
                device = comms.connect(str(ip))
                found.append({
                    "ip": str(ip),
                    "device info": comms.receive(device)
                })

    with open(OUTPUT_FILE, "w") as f:
        json.dump(found, f, indent=4)

    return found

def start_periodic_scan():
    scan_thread = threading.Thread(target=_periodic_scan, daemon=True)
    scan_thread.start()
    return scan_thread

def _periodic_scan():
    while True:
        scan_network()
        time.sleep(SCAN_INTERVAL)
