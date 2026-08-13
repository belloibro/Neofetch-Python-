import socket
import concurrent.futures
import json
from datetime import datetime

target = "127.0.0.1"
# Expanded common port range
ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 1433, 3306, 3389, 8080, 8443]

def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        result = s.connect_ex((target, port))
        if result == 0:
            banner = "Active"
            try:
                s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = s.recv(512).decode('utf-8', errors='ignore').split('\n')[0]
            except Exception:
                pass
            print(f"[+] Port {port}: OPEN")
            return {"port": port, "status": "OPEN", "service_info": banner}
        s.close()
    except Exception:
        pass
    return None

def run_audit():
    print(f"[*] Starting Broad Recon Audit on {target} at {datetime.now()}...")
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_port = {executor.submit(scan_port, p): p for p in ports}
        for future in concurrent.futures.as_completed(future_to_port):
            res = future.result()
            if res:
                results.append(res)
    
    report = {
        "timestamp": str(datetime.now()),
        "target": target,
        "total_open": len(results),
        "results": results
    }
    
    with open("/data/data/com.termux/files/home/scripts/audit_report.json", "w") as f:
        json.dump(report, f, indent=4)
    print(f"[*] Audit Complete. Found {len(results)} open ports. Saved to ~/scripts/audit_report.json.")

if __name__ == "__main__":
    run_audit()
