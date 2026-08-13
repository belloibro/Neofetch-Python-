import os
import shutil
from datetime import datetime

archive_dir = "/data/data/com.termux/files/home/scripts/archive"
os.makedirs(archive_dir, exist_ok=True)

report_path = "/data/data/com.termux/files/home/scripts/audit_report.json"

if os.path.exists(report_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"audit_report_{timestamp}.json"
    shutil.copy(report_path, os.path.join(archive_dir, backup_name))
    print(f"[*] Archived previous report as {backup_name}")
else:
    print("[!] No active report found to archive.")
