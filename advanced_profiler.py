import socket
import concurrent.futures

target = "127.0.0.1"
target_ports = range(1, 1025)

def check_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        if s.connect_ex((target, port)) == 0:
            s.close()
            return port
    except Exception:
        pass
    return None

print(f"[*] Scanning extended port range (1-1024) on {target}...")
open_ports = []

with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    futures = [executor.submit(check_port, p) for p in target_ports]
    for future in concurrent.futures.as_completed(futures):
        res = future.result()
        if res:
            open_ports.append(res)

print(f"\n[+] Scan finished. Open ports discovered: {sorted(open_ports)}")
