#!/usr/bin/env bash
echo "[*] Starting packet capture on any interface..."
tcpdump -i any -w ~/scripts/capture.pcap
