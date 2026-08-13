import socket
import concurrent.futures
from datetime import datetime

def ping_host(ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        result = s.connect_ex((ip, 80)) # checking common port or adjust as needed
        if result == 0 or result == 111: # 111 connection refused means host is up
            print(f"[+] Active Host Found: {ip}")
            return ip
        s.close()
    except Exception:
        pass
    return None

def scan_subnet():
    base_ip = "192.168.1."
    print(f"[*] Scanning subnet {base_ip}1-254...")
    active_hosts = []
    
    ips = [f"{base_ip}{i}" for i in range(1, 255)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(ping_host, ips)
        for r in results:
            if r:
                active_hosts.append(r)
                
    print(f"[*] Subnet scan complete. Found {len(active_hosts)} active hosts.")

if __name__ == "__main__":
    scan_subnet()
