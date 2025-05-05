from wallet.manager import WalletManager
from database.crud.wallet.wallet_history_ops import create_wallet_history
from exchanges.jupiter.price import getJupPrice
from global_config import WALLET_PRIV_KEY, WALLET_PUB_KEY, WSOL


if __name__ == "__main__":

    my_wallet = WalletManager(WALLET_PUB_KEY, WALLET_PRIV_KEY)
    wallet_assets = my_wallet.get_assets()
    
    wallet_usd_value = 0
    for token in wallet_assets:
        # Toekn Info
        token_balance = token.get("balance", 0) / 10 ** token.get("decimals", 0)
        token_mint = token.get("mint", "")

        # Token USD Value
        token_price = getJupPrice(token_mint).get(token_mint, {}).get("price", 0)
        token_usd_value = float(token_price) * token_balance

        # Wallet USD Value
        wallet_usd_value += token_usd_value
    
    sol_price = getJupPrice(WSOL).get(WSOL, {}).get("price", 0)
    wallet_sol_value = wallet_usd_value / float(sol_price)
    create_wallet_history(
        balance_usdt=round(wallet_usd_value,3),
        balance_sol=round(wallet_sol_value,5)
    )
