import json

try:
    with open("/data/data/com.termux/files/home/scripts/audit_report.json", "r") as f:
        data = json.load(f)
    print("=== RECON AUDIT REPORT ===")
    print(f"Timestamp : {data['timestamp']}")
    print(f"Target    : {data['target']}")
    print(f"Open Ports: {data['total_open']}")
    print("-" * 30)
    for item in data['results']:
        print(f"Port {item['port']} -> Status: {item['status']} | Info: {item['service_info']}")
except FileNotFoundError:
    print("[!] No audit report found.")
