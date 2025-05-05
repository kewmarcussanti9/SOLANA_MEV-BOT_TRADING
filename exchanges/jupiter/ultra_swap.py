import requests, json, base64
from solders.transaction import VersionedTransaction


base_url = "https://lite-api.jup.ag/ultra/v1"


def get_order(input_mint: str, output_mint: str, amount: str, wallet_pub_key: str):
    payload = {
        'inputMint': input_mint,
        'outputMint': output_mint,
        'amount': amount,
        'taker': wallet_pub_key
        }
    headers = {'Accept': 'application/json'}

    response = requests.get(url=f"{base_url}/order", params=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def sign_transaction(payer, transaction: str):
    # Deserialize the transaction
    transaction_bytes = base64.b64decode(transaction)
    unsigned_tx = VersionedTransaction.from_bytes(transaction_bytes)
    
    # Sign the trasaction message
    msg = unsigned_tx.message
    signature = payer.sign_message(bytes(msg))

    # Sign Trasaction
    signed_tx = VersionedTransaction.populate(msg, [signature])

    # Serialize the transaction to base64 format
    serialized_transaction = bytes(signed_tx)
    return base64.b64encode(serialized_transaction).decode('utf-8')

"""
/!\ Problem to solve => HTTP Error: 504 Gateway Timeout
"""
def execute(signed_tx: str, request_id: str):
    payload = json.dumps({
        "signedTransaction": signed_tx,
        "requestId": request_id
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.post(url=f"{base_url}/execute", headers=headers, data=payload)
    response.raise_for_status()
    return response.json()
