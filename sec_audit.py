import socket
import os
import sys
import platform
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

def banner():
    b = "\n".join([
        "=" * 60,
        "      ADVANCED SECURITY & RECON SUITE [ULTIMATE]      ",
        "      Ethical Hacking & Environment Auditor       ",
        "=" * 60
    ])
    print(f"\033[1;32m{b}\033[0m")
    return b

def audit_environment():
    output = []
    output.append("\n[*] Auditing Execution Environment...")
    output.append(f"[-] Operating System : {platform.system()} {platform.release()}")
    output.append(f"[-] Architecture     : {platform.machine()}")
    output.append(f"[-] Python Version   : {platform.python_version()}")
    try:
        user = os.getlogin()
    except Exception:
        user = "sandbox_user"
    output.append(f"[-] Current User     : {user}")
    
    is_root = os.getuid() == 0 if hasattr(os, 'getuid') else False
    if is_root:
        output.append("[!] WARNING: Running with elevated (Root/Superuser) privileges!")
    else:
        output.append("[+] Running in unprivileged sandbox/user mode.")
    
    output.append("\n[*] Network Interfaces & IP Configuration:")
    try:
        ifconfig_res = os.popen("ip addr show 2>/dev/null || ifconfig 2>/dev/null").read()
        if ifconfig_res.strip():
            output.append(ifconfig_res)
        else:
            output.append("[-] Interface command unavailable.")
    except Exception:
        output.append("[-] Could not retrieve network interfaces.")

    text = "\n".join(output)
    print(text)
    return text

def probe_http_endpoints(ip, port):
    endpoints = ["/", "/health", "/status", "/api", "/admin", "/login"]
    discovered = []
    for path in endpoints:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((ip, port))
            request = f"GET {path} HTTP/1.1\r\nHost: {ip}\r\nConnection: close\r\n\r\n"
            s.sendall(request.encode())
            response = s.recv(512).decode('utf-8', errors='ignore')
            s.close()
            
            if response:
                first_line = response.split('\r\n')[0]
                if any(code in first_line for code in ["200", "301", "302", "401", "403"]):
                    discovered.append(f"{path} [{first_line}]")
        except Exception:
            pass
    return discovered

def grab_banner_and_assets(ip, port):
    details = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.8)
        s.connect((ip, port))
        if port in [80, 443, 3000, 5000, 8080, 8443]:
            s.sendall(b"HEAD / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        banner_data = s.recv(1024).decode('utf-8', errors='ignore').strip()
        s.close()
        if banner_data:
            first_line = banner_data.split('\n')[0]
            details.append(f"Banner: {first_line}")
    except Exception:
        pass

    if port in [80, 443, 3000, 5000, 8080, 8443]:
        endpoints = probe_http_endpoints(ip, port)
        if endpoints:
            details.append(f"Endpoints: {', '.join(endpoints)}")

    if details:
        return f" | { ' | '.join(details) }"
    return ""

def test_single_port(target, port, service, skip_banner):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.3)
    try:
        result = s.connect_ex((target, port))
        if result == 0:
            extra_info = "" if skip_banner else grab_banner_and_assets(target, port)
            return port, f"{port:<8} {'OPEN':<12} {service}{extra_info}"
        else:
            return port, f"{port:<8} {'CLOSED':<12} {service}"
    except Exception:
        return port, f"{port:<8} {'CLOSED':<12} {service}"
    finally:
        s.close()

def local_port_scanner(target, skip_banner=False):
    output = []
    output.append(f"\n[*] Running Ultimate Multi-Threaded Recon on Target: {target}...")
    common_ports = {
        21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS", 
        3000: "Node-Dev", 5000: "Flask-Dev", 8080: "HTTP-Proxy", 
        8443: "HTTPS-Alt", 5037: "ADB-Server"
    }
    
    output.append(f"{'PORT':<8} {'STATUS':<12} {'SERVICE & DISCOVERED ASSETS'}")
    output.append("-" * 70)
    
    results_dict = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(test_single_port, target, port, service, skip_banner): port for port, service in common_ports.items()}
        for future in as_completed(futures):
            port, line = future.result()
            results_dict[port] = line
            
    for port in sorted(results_dict.keys()):
        output.append(results_dict[port])

    text = "\n".join(output)
    print(text)
    return text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Security & Recon Suite for Termux")
    parser.add_argument("-t", "--target", default="127.0.0.1", help="Target IP address or hostname to scan (default: 127.0.0.1)")
    parser.add_argument("--fast", action="store_true", help="Skip service banner and endpoint grabbing")
    parser.add_argument("--nolog", action="store_true", help="Do not save the output to a text report file")
    args = parser.parse_args()

    report_lines = []
    report_lines.append(banner())
    report_lines.append(audit_environment())
    report_lines.append(local_port_scanner(target=args.target, skip_banner=args.fast))
    report_lines.append("\n[+] Reconnaissance completed successfully.")
    print("\n[+] Reconnaissance completed successfully.")

    if not args.nolog:
        filename = f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w") as f:
            f.write("\n".join(report_lines))
        print(f"[+] Report successfully saved to {filename}")
