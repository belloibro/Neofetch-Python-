import json
import socket
import subprocess
import sys

target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
open_ports_list = []

for port in [21, 22, 80, 443, 3306, 8080]:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.4)
    try:
        if s.connect_ex((target, port)) == 0:
            open_ports_list.append({"port": port, "status": "open"})
    except:
        pass
    s.close()

risky_found = []
try:
    ps_output = subprocess.run(["ps", "aux"], capture_output=True, text=True).stdout
    for keyword in ["nc", "ncat", "telnet", "ssh"]:
        if keyword in ps_output:
            risky_found.append(keyword)
except:
    pass

report = {
    "target": target,
    "total_open": len(open_ports_list),
    "ports": open_ports_list,
    "risky_processes": risky_found
}

with open("audit_report.json", "w") as f:
    json.dump(report, f)
