import json
import urllib.request
import urllib.parse

def send_alert():
    token = "YOUR_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"
    
    try:
        with open("/data/data/com.termux/files/home/scripts/audit_report.json", "r") as f:
            data = json.load(f)
            
        message = f"🚨 *Security Audit Alert*\n\nTarget: `{data['target']}`\nOpen Ports Found: `{data['total_open']}`\nTimestamp: `{data['timestamp']}`"
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = urllib.parse.urlencode({"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}).encode("utf-8")
        
        req = urllib.request.Request(url, data=payload)
        with urllib.request.urlopen(req) as response:
            print("[*] Telegram alert sent successfully.")
    except Exception as e:
        print(f"[!] Failed to send alert: {e}")

if __name__ == "__main__":
    send_alert()
