#!/usr/bin/env python3
"""
Automated GitHub Contribution Bot Script
Updates the contribution log with timestamp and run details.
"""

from datetime import datetime
import os

LOG_FILE = "contributions.log"

def update_contribution():
    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    log_entry = f"Commit on {timestamp_str}\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
        
    print(f"[+] Updated {LOG_FILE}: {log_entry.strip()}")

if __name__ == "__main__":
    update_contribution()
