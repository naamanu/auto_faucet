#!/usr/bin/env python3
import os
import time
import requests
import logging
from dataclasses import dataclass
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

log = logging.getLogger(__name__)

load_dotenv()


@dataclass
class Config:
    api_key: str
    addresses: list[str]
    blockchain: str = "SOL-DEVNET"
    interval_hours: float = 2.0
    api_url: str = "https://api.circle.com/v1/faucet/drips"

    @classmethod
    def from_env(cls) -> "Config":
        load_dotenv()
        return cls(
            api_key=os.getenv("CIRCLE_API_KEY", ""),
            addresses=[
                a.strip() for a in os.getenv("ADDRESSES", "").split(",") if a.split()
            ],
            blockchain=os.getenv("BLOCKCHAIN", "SOL-DEVNET"),
            interval_hours=float(os.getenv("INTERVAL_HOURS", "2")),
        )


class AutoFaucet:
    def __init__(self, config: Config) -> None:
        self.config = config
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _truncate_address(self, address: str) -> str:
        return f"{address[:8]}...{address[-4:]}"

    def claim_usdc(self, address):
        payload = {
            "address": address,
            "blockchain": self.config.blockchain,
            "usdc": True,
        }

        short_addr = self._truncate_address(address)

        try:
            resp = self._session.post(self.config.api_url, json=payload, timeout=30)
            if resp.status_code == 200:
                log.info(f"SUCCESS: Claimed USDC for {short_addr}")
                return True
            else:
                log.warning(f"FAILED: {short_addr} - {resp.status_code}: {resp.text}")
                return False
        except requests.RequestException as e:
            log.error(f"ERROR: {short_addr} - {e}")
            return False

    def run_claims(
        self,
    ):
        log.info(
            f"Starting claims for {len(self.config.addresses)} address(es) on {self.config.blockchain}"
        )
        for addr in self.config.addresses:
            self.claim_usdc(addr)
        log.info(f"Done. Next run in {self.config.interval_hours} hours.")


def main():
    config = Config.from_env()
    if not config.api_key:
        log.error("Error: CIRCLE_API_KEY not set in .env")
        return
    if not config.addresses:
        log.error("Error: ADDRESSES not set in .env")
        return

    log.info("Circle USDC Faucet Auto-Claimer started")
    log.info(
        f"Addresses: {config.addresses} | Blockchain: {config.blockchain} | Interval: {config.interval_hours}h"
    )

    faucet = AutoFaucet(config)
    while True:
        faucet.run_claims()
        time.sleep(config.interval_hours * 3600)


if __name__ == "__main__":
    main()
