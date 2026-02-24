import requests
import json

# ClawVault Phase 1: Solana RPC Connection PoC
# This script demonstrates the ingestion layer of our architecture

def get_solana_stats():
    # Using a public Helius/Alchemy style RPC endpoint
    url = "https://api.mainnet-beta.solana.com"
    
    headers = {'Content-Type': 'application/json'}
    
    # Request 1: Get latest slot (Block Height)
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSlot"
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        slot = response.json()['result']
        print(f"--- ClawVault Data Ingestion PoC ---")
        print(f"Successfully connected to Solana Mainnet.")
        print(f"Current Slot (Bronze Layer): {slot}")
        print(f"Status: Ingestion Pipeline Ready.")
    except Exception as e:
        print(f"Error connecting to RPC: {e}")

if __name__ == "__main__":
    get_solana_stats()
