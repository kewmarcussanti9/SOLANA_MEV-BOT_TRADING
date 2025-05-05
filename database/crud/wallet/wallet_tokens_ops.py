from decimal import Decimal
from typing import Optional, List
from database.connection import get_cursor
from database.models.wallet import WalletToken


def insert_wallet_token(mint: str, symbol: str, usdt_value: Decimal = None,
                        purchase_price: Optional[Decimal] = None) -> int:
    with get_cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO wallet_token (mint, symbol, purchase_price, usdt_value)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (mint, symbol, purchase_price, usdt_value)
        )
        return cursor.fetchone()['id']

def get_wallet_token(mint: str = None) -> Optional[WalletToken]:
    with get_cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM wallet_token 
            WHERE mint = %s
            """,
            (mint,)
        )
        data = cursor.fetchone()
        
        if data:
            return WalletToken(
                id=data['id'],
                mint=data['mint'],
                symbol=data['symbol'],
                purchase_price=data['purchase_price'],
                usdt_value=data['usdt_value']
            )
        return None

def get_all_wallet_tokens() -> List[WalletToken]:
    with get_cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM wallet_token
            ORDER BY symbol
            """
        )
        
        return [
            WalletToken(
                id=row['id'],
                mint=row['mint'],
                symbol=row['symbol'],
                purchase_price=row['purchase_price'],
                usdt_value=row['usdt_value']
            )
            for row in cursor.fetchall()
        ]

def update_wallet_token(token_id: int = None, mint: str = None, usdt_value: Decimal = None,
                       symbol: str = None, purchase_price: Decimal = None) -> bool:
    if token_id is None and mint is None:
        raise ValueError("You must provide either token_id or mint")
    
    update_fields = []
    params = []
    
    if symbol is not None:
        update_fields.append("symbol = %s")
        params.append(symbol)

    if usdt_value is not None:
        update_fields.append("usdt_value = %s")
        params.append(usdt_value)
        
    if purchase_price is not None:
        update_fields.append("purchase_price = %s")
        params.append(purchase_price)
        
    if not update_fields:
        return False
    
    with get_cursor() as cursor:
        if token_id is not None:
            params.append(token_id)
            cursor.execute(
                f"""
                UPDATE wallet_token
                SET {', '.join(update_fields)}
                WHERE id = %s
                """,
                tuple(params)
            )
        else:
            params.append(mint)
            cursor.execute(
                f"""
                UPDATE wallet_token
                SET {', '.join(update_fields)}
                WHERE mint = %s
                """,
                tuple(params)
            )
        
        return cursor.rowcount > 0

def delete_wallet_token(token_id: int = None, mint: str = None) -> bool:
    if token_id is None and mint is None:
        raise ValueError("You must provide either token_id or mint")
    
    with get_cursor() as cursor:
        if token_id is not None:
            cursor.execute(
                """
                DELETE FROM wallet_token
                WHERE id = %s
                """,
                (token_id,)
            )
        else:
            cursor.execute(
                """
                DELETE FROM wallet_token
                WHERE mint = %s
                """,
                (mint,)
            )
        
        return cursor.rowcount > 0

def delete_all_wallet_tokens() -> bool:
    with get_cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM wallet_token
            """
        )
        return cursor.rowcount > 0
