import time
import os
import sys
import threading
import requests
import subprocess
import sqlite3
import json
from datetime import datetime

TOKEN = "8837972883:AAGS5-uwckm72yklahipTYHhngzswSWBlMk"
CHAT_ID = "8729011687"
URL = f"https://api.telegram.org/bot{TOKEN}"
DB_PATH = "security_audit.db"
REPORT_PATH = "audit_report.json"
AUDIT_SCRIPT = "/data/data/com.termux/files/home/scripts/auto_audit.py"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            target TEXT,
            open_ports INTEGER,
            details TEXT
        )
    ''')
    conn.commit()
    conn.close()

def prune_old_logs():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM scans WHERE timestamp < datetime('now', '-30 days')")
        conn.commit()
        conn.close()
    except Exception:
        pass

def get_last_scan(target):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT open_ports FROM scans WHERE target = ? ORDER BY timestamp DESC LIMIT 1", (target,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def log_scan_to_db(target, open_ports, details):
    prune_old_logs()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scans (timestamp, target, open_ports, details) VALUES (?, ?, ?, ?)",
                   (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), target, open_ports, json.dumps(details)))
    conn.commit()
    conn.close()

def send_message(text):
    try:
        requests.post(f"{URL}/sendMessage", json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
    except Exception:
        pass

def get_updates(offset=None):
    try:
        response = requests.get(f"{URL}/getUpdates", params={"offset": offset, "timeout": 30})
        return response.json().get("result", [])
    except Exception:
        return []

def run_audit_logic(target="127.0.0.1"):
    subprocess.run(["python3", "auto_audit.py", target], capture_output=True, text=True)
    details = {}
    total_open = 0
    try:
        if os.path.exists(REPORT_PATH):
            with open(REPORT_PATH, "r") as f:
                report_data = json.load(f)
                target = report_data.get("target", target)
                total_open = report_data.get("total_open", 0)
                details = report_data.get("ports", [])
    except Exception:
        pass
    
    previous_open = get_last_scan(target)
    log_scan_to_db(target, total_open, details)
    
    is_threat = False
    if previous_open is not None and total_open > previous_open:
        is_threat = True
        
    return target, total_open, details, is_threat

def background_scheduler():
    while True:
        time.sleep(14400)
        try:
            target, total_open, _, is_threat = run_audit_logic("127.0.0.1")
            if is_threat:
                send_message(f"🚨 *SECURITY ALERT: New Open Ports Found!*\n🎯 Target: `{target}`\n🔓 Open Ports: `{total_open}` (Increased!)")
            else:
                send_message(f"⏰ *Automated Background Audit Complete*\n🎯 Target: `{target}`\n🔓 Open Ports: `{total_open}` (Stable)")
        except Exception:
            pass

init_db()
threading.Thread(target=background_scheduler, daemon=True).start()
print("[*] Elite Production Bot Listener Active (Dynamic Targets + Pruning + Diffing + Push)...")
offset = None

while True:
    updates = get_updates(offset)
    for update in updates:
        offset = update["update_id"] + 1
        message = update.get("message", {})
        text = message.get("text", "")
        sender_chat = str(message.get("chat", {}).get("id", ""))
        
        if sender_chat == CHAT_ID:
            if text.startswith("/scan"):
                parts = text.split()
                custom_target = parts[1] if len(parts) > 1 else "127.0.0.1"
                send_message(f"🔍 *Running security audit on target:* `{custom_target}`...")
                try:
                    target, total_open, _, is_threat = run_audit_logic(custom_target)
                    if is_threat:
                        send_message(f"🚨 *ALERT: Threat Diff Detected!*\n🎯 Target: `{target}`\n🔓 Open Ports: `{total_open}` (Higher than previous scan!)")
                    else:
                        send_message(f"✅ *Scan complete on {target}*\n🔓 Open Ports Found: `{total_open}`")
                except Exception as e:
                    send_message(f"[!] Scan failed: {e}")
            elif text == "/ports":
                send_message("🔎 *Fetching latest port breakdown & system risks...*")
                try:
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute("SELECT timestamp, target, open_ports, details FROM scans ORDER BY timestamp DESC LIMIT 1")
                    row = cursor.fetchone()
                    conn.close()
                    if row:
                        msg = f"📊 *Latest Security Breakdown:*\n📅 *Time:* {row[0]}\n🎯 *Target:* {row[1]}\n🔓 *Ports Open:* {row[2]}\n📝 *Details:* `{row[3]}`"
                    else:
                        msg = "📭 No detailed port data found."
                    send_message(msg)
                except Exception as e:
                    send_message(f"[!] Failed to fetch ports: {e}")
            elif text == "/dev":
                send_message("💻 *Fetching Git & Workspace status...*")
                try:
                    branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip() or "main"
                    last_commit = subprocess.run(["git", "log", "-1", "--pretty=format:%h - %s"], capture_output=True, text=True).stdout.strip() or "No commits yet"
                    status = subprocess.run(["git", "status", "--short"], capture_output=True, text=True).stdout.strip()
                    msg = f"💻 *Developer Workspace Status:*\n🌿 *Branch:* `{branch}`\n📌 *Last Commit:* `{last_commit}`\n⚡ *Modified Files:*\n```{status if status else 'Working tree clean'}```"
                    send_message(msg)
                except Exception as e:
                    send_message(f"[!] Dev status check failed: {e}")
            elif text == "/push":
                send_message("🚀 *Pushing updates to GitHub repository...*")
                try:
                    subprocess.run(["git", "add", "."], capture_output=True, text=True)
                    subprocess.run(["git", "commit", "-m", "Autonomous update via Telegram bot"], capture_output=True, text=True)
                    push_res = subprocess.run(["git", "push"], capture_output=True, text=True)
                    if push_res.returncode == 0:
                        send_message("✅ *Successfully pushed code changes to GitHub!*")
                    else:
                        send_message(f"⚠️ *Git Push status:*\n```{push_res.stdout or push_res.stderr}```")
                except Exception as e:
                    send_message(f"[!] GitHub push failed: {e}")
            elif text == "/stats":
                send_message("📊 *Fetching scan history...*")
                try:
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute("SELECT timestamp, target, open_ports FROM scans ORDER BY timestamp DESC LIMIT 5")
                    rows = cursor.fetchall()
                    conn.close()
                    if rows:
                        msg = "📜 *Recent Scan History:*\n\n"
                        for row in rows:
                            msg += f"📅 *Time:* {row[0]}\n🎯 *Target:* {row[1]}\n🔓 *Open Ports:* {row[2]}\n\n"
                    else:
                        msg = "📭 No scan history found."
                    send_message(msg)
                except Exception as e:
                    send_message(f"[!] Failed to fetch stats: {e}")
            elif text == "/status":
                send_message("🟢 *Elite Agent Online: Dynamic Target Scanning, Log Pruning, Threat Diffing, GitHub Sync & Dev Controls Active.*")
            elif text == "/restart":
                send_message("🔄 *Restarting bot service...*")
                os.execv(sys.executable, ['python3'] + sys.argv)
    time.sleep(2)
