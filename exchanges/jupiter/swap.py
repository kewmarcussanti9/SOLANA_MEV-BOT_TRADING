import requests, base64, json, re

from solders import message
from solders.transaction import VersionedTransaction

from solana.rpc.core import RPCException
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Processed, Finalized
from solana.rpc.async_api import AsyncClient

from global_config import SOL_URI, HELIUS_RPC


base_url = "https://lite-api.jup.ag/swap/v1"


def get_quote(inputMint: str, outputMint: str, amount: int, slippageBps: int=500, dynamicSlippage: bool=False):
    """
    slippageBps = 500 ==> slippage of 5%
    """
    url = f'{base_url}/quote?'
    params = {
        'inputMint': inputMint,
        'outputMint': outputMint,
        'amount': amount,
        'slippageBps': slippageBps
    }
    if dynamicSlippage:
        params['dynamicSlippage'] = 'true'
    
    quote_url = url + '&'.join([f"{key}={value}" for key, value in params.items()])
    response = requests.get(quote_url)
    response.raise_for_status()

    quote_data = response.json()
    if quote_data.get("errorCode") not in ["TOKEN_NOT_TRADABLE", "COULD_NOT_FIND_ANY_ROUTE"]:
        return quote_data
    else:
        raise Exception(f"[get_quote] Error getting quote: {quote_data.get('errorCode')}")

def build_transaction(wallet_pub_key: str, quote: dict):
    payload = {
        "userPublicKey": wallet_pub_key,
        "quoteResponse": quote,
        "wrapAndUnwrapSol": True
        }
    headers = {'Content-Type': 'application/json'}
    swap_response = requests.post(f'{base_url}/swap', json=payload, headers=headers)
    swap_response.raise_for_status()
    return swap_response.json().get("swapTransaction")

async def send_transaction(payer, swap_transaction):
    try:
        # Deserialize the transaction
        transaction = VersionedTransaction.from_bytes(base64.b64decode(swap_transaction))
        # Sign the trasaction message
        signature = payer.sign_message(message.to_bytes_versioned(transaction.message))
        # Sign Trasaction
        signed_tx = VersionedTransaction.populate(transaction.message, [signature])

        async with AsyncClient(SOL_URI) as async_client:
            opts = TxOpts(skip_preflight=False, preflight_commitment=Processed, max_retries=2)
            tx_id = await async_client.send_raw_transaction(txn=bytes(signed_tx), opts=opts)
            result = json.loads(tx_id.to_json()).get('result')
            return result          #txid.value
    except RPCException as e:
        # Extract the message
        msg = re.search(r'message: "(.*?)"', e)
        msg = msg.group(1) if msg else "No message found"
        # Extract the error message
        error_message = re.search(r'Error Message: (.*?)\.', e)
        error_message = error_message.group(1) if error_message else "No error message found"
        print(f"RPC Error: \n- {msg} \n- {error_message}")
    except Exception as e:
        print(f"Error during swap transaction : {e}")
