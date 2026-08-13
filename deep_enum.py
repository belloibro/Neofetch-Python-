import socket

target = "127.0.0.1"
ports_probes = {
    21: b"HELP\r\n",
    22: b"SSH-2.0-Custom\r\n",
    80: b"GET / HTTP/1.0\r\n\r\n",
    443: b"GET / HTTP/1.0\r\n\r\n",
    8080: b"GET / HTTP/1.0\r\n\r\n"
}

print(f"[*] Starting deep service enumeration on {target}...")

for port, probe in ports_probes.items():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        s.connect((target, port))
        s.sendall(probe)
        banner = s.recv(1024).decode('utf-8', errors='ignore')
        if banner:
            print(f"\n[+] Port {port} Service Response:\n{banner.strip()}")
        s.close()
    except Exception:
        pass
