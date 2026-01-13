# auto_faucet

*claim your stables..automagically*

Automatically claim 1 USDC every 2 hours from Circle's testnet faucet.

## Quick Start (< 60 seconds)

1. Get a free API key at [console.circle.com](https://console.circle.com)

2. Setup:
```bash
pip install -r requirements.txt
cp .env.example .env
```

3. Edit `.env` with your API key and wallet addresses

4. Run:
```bash
python faucet.py
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `CIRCLE_API_KEY` | Your Circle TEST API key | Required |
| `ADDRESSES` | Comma-separated wallet addresses | Required |
| `BLOCKCHAIN` | Network identifier | `SOL-DEVNET` |
| `INTERVAL_HOURS` | Hours between claims | `2` |

## Supported Networks

- `SOL-DEVNET` - Solana Devnet
- `ETH-SEPOLIA` - Ethereum Sepolia
- `ARB-SEPOLIA` - Arbitrum Sepolia
- `BASE-SEPOLIA` - Base Sepolia
- `MATIC-AMOY` - Polygon Amoy

## Run in Background

```bash
nohup python faucet.py > faucet.log 2>&1 &
```

## License

MIT
