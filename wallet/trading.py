import asyncio
from wallet.manager import WalletManager
from exchanges.jupiter.price import getJupPrice
from database.crud.wallet.wallet_tokens_ops import insert_wallet_token, delete_wallet_token
from database.crud.wallet.wallet_tokens_ops import get_wallet_token, get_all_wallet_tokens
from database.crud.wallet.trading_history_ops import create_trading_history
from global_config import WALLET_PRIV_KEY, WALLET_PUB_KEY, WSOL, USDC


async def main():
    my_wallet = WalletManager(WALLET_PUB_KEY, WALLET_PRIV_KEY)
    wallet_assets = my_wallet.get_assets()
    wallet_mints = [token.get("mint", "") for token in wallet_assets]

    db_wallet_assets = get_all_wallet_tokens()
    for db_token in db_wallet_assets:
        if db_token.mint not in wallet_mints:
            # Delete token from DB
            delete_wallet_token(token_id=db_token.id)

    db_wallet_assets = get_all_wallet_tokens()
    db_mints = [db_token.mint for db_token in db_wallet_assets]
    for token in wallet_assets:
        token_actual_price = float(getJupPrice(token["mint"]).get(token["mint"], {}).get("price", 0))
        token_usd_value = token_actual_price * (token.get("balance", 0) / 10 ** token.get("decimals", 0))
        # Check if token already exists in DB
        if token["mint"] not in db_mints:
            # Insert new token into DB
            insert_wallet_token(
                mint=token["mint"],
                symbol=token["symbol"],
                purchase_price=token_actual_price,
                usdt_value=token_usd_value
            )
        else:
            if token["mint"] in [WSOL, USDC]:
                continue
            db_token = get_wallet_token(mint=token["mint"])

            threshold_upper = 1.8 * float(db_token.purchase_price)
            threshold_lower = 0.5 * float(db_token.purchase_price)

            if token_actual_price >= threshold_upper or token_actual_price <= threshold_lower:
                result = await my_wallet.sell_token(mint=token["mint"], pct_amount=100)
                if result.get("status"):
                    create_trading_history(
                        mint=token["mint"],
                        symbol=token["symbol"], 
                        usdt_value=token_usd_value,
                        buy_price=float(db_token.purchase_price),
                        sell_price=token_actual_price
                    )
                    print(token["symbol"], "sold!")
                else:
                    print(token["symbol"], ": Transaction failed!")


asyncio.run(main())