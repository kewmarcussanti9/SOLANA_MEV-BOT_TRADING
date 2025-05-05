import requests
from solders.pubkey import Pubkey
from solders.signature import Signature
from solana.rpc.api import Client
from global_config import SOL_URI


sol_client = Client(SOL_URI)


def get_wallet_signatures(public_key, before=None, until=None, limit=None, commitment='finalized'):
    """
    Get all signatures for a given wallet address
     - public_key: Wallet address
     - before: Signature to start from
     - until: Signature to end at
     - limit: Number of signatures to return
     - commitment: Commitment level
    :return: List of signatures
    """
    try:
        wallet = Pubkey.from_string(public_key)
        if before:
            before = Signature.from_string(before)
        if until:
            until = Signature.from_string(until)
        signatures = sol_client.get_signatures_for_address(wallet, before=before, until=until, limit=limit, commitment=commitment)
        return [str(sig.signature) for sig in signatures.value if sig.err is None]
    except Exception as e:
        print(f"[Get Wallet Signatures] {e}")
        return []


def get_signature_status(tx_signature: str) -> bool:
    """
    Get the status of a transaction
     - tx_signature: Transaction signature
    :return: True if the transaction is finalized, False otherwise
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignatureStatuses",
        "params": [
            [tx_signature],
            {"searchTransactionHistory": True}
        ]
    }
    response = requests.post(SOL_URI, json=payload)
    status = response.json()['result']['value'][0]
    if status is None:
        print(f"Transaction '{tx_signature}' not found")
        return False
    elif status['confirmationStatus'] == 'finalized':
        print(f"Transaction '{tx_signature}' is finalized")
        return True
    else:
        print(f"Transaction '{tx_signature}' is not finalized yet. Current status: {status['confirmationStatus']}")
        return False
