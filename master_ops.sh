#!/usr/bin/env bash
echo "=========================================="
echo "    MOBILE DEV & SECURITY OPERATIONS"
echo "=========================================="

echo "[*] Running network check..."
if command -v ip &> /dev/null; then
    ip route show
else
    ifconfig
fi

echo "[*] Checking local ports with nmap..."
nmap -p 22,80,443 127.0.0.1

echo "[*] Checking local Git repositories..."
if [ -d "$HOME/projects" ]; then
    for repo in "$HOME/projects"/*; do
        if [ -d "$repo/.git" ]; then
            echo "[+] Syncing repository: $(basename "$repo")"
            cd "$repo"
            git add .
            git commit -m "Auto-sync update: $(date +%Y-%m-%d_%H-%M-%S)"
            git push origin main 2>/dev/null || echo "[-] Push skipped or no remote set for $(basename "$repo")"
            cd ~/scripts
        fi
    done
fi

echo "=========================================="
echo "    AUTOMATION ROUTINE COMPLETE"
echo "=========================================="
python3 ~/scripts/bot_notify.py


python3 ~/scripts/bot_notify.py
python3 ~/scripts/bot_notify.py
python3 ~/scripts/bot_notify.py
