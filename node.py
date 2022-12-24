from algosdk.v2client import algod
import json

algod_address = "https://testnet-api.algonode.network"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token, algod_address)

status = algod_client.status()
print(json.dumps(status, indent=4))