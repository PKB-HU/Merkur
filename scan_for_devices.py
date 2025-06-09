import socket
import ipaddress
import concurrent.futures

PORT_TO_SCAN = 6274
TIMEOUT = 1  # seconds

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
    print(f"Scanning subnet: {subnet} for port {PORT_TO_SCAN}...\n")

    found = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, str(ip)): ip for ip in subnet.hosts()}
        for future in concurrent.futures.as_completed(futures):
            ip = futures[future]
            result = future.result()
            if result:
                found.append(str(ip))

    '''
    if found:
        print("Devices with port 6274 open:")
        for ip in found:
            print(f"{ip}")
    else:
        print("No devices found with port 6274 open.")
    '''
    return found

