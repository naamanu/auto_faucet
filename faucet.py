#!/usr/bin/env python3
import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.circle.com/v1/faucet/drips"
API_KEY = os.getenv("CIRCLE_API_KEY", "")
ADDRESSES = [a.strip() for a in os.getenv("ADDRESSES", "").split(",") if a.strip()]
BLOCKCHAIN = os.getenv("BLOCKCHAIN", "SOL-DEVNET")
INTERVAL_HOURS = float(os.getenv("INTERVAL_HOURS", "2"))


def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")


def claim_usdc(address):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "address": address,
        "blockchain": BLOCKCHAIN,
        "usdc": True,
    }
    try:
        resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        if resp.status_code == 200:
            log(f"SUCCESS: Claimed USDC for {address[:8]}...{address[-4:]}")
            return True
        else:
            log(f"FAILED: {address[:8]}...{address[-4:]} - {resp.status_code}: {resp.text}")
            return False
    except Exception as e:
        log(f"ERROR: {address[:8]}...{address[-4:]} - {e}")
        return False


def run_claims():
    log(f"Starting claims for {len(ADDRESSES)} address(es) on {BLOCKCHAIN}")
    for addr in ADDRESSES:
        claim_usdc(addr)
    log(f"Done. Next run in {INTERVAL_HOURS} hours.")


def main():
    if not API_KEY:
        print("Error: CIRCLE_API_KEY not set in .env")
        return
    if not ADDRESSES:
        print("Error: ADDRESSES not set in .env")
        return

    log(f"Circle USDC Faucet Auto-Claimer started")
    log(f"Addresses: {len(ADDRESSES)} | Blockchain: {BLOCKCHAIN} | Interval: {INTERVAL_HOURS}h")

    while True:
        run_claims()
        time.sleep(INTERVAL_HOURS * 3600)


if __name__ == "__main__":
    main()
