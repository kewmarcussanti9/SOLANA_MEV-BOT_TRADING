from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from database.connection import get_cursor
from database.models.wallet import TradingHistory


def create_trading_history(mint: str, symbol: str, usdt_value: Decimal,
                           buy_price: Optional[Decimal] = None, sell_price: Optional[Decimal] = None,
                           date: Optional[datetime] = None) -> int:
    if date is None:
        date = datetime.now()
        
    with get_cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO trading_history (mint, symbol, buy_price, sell_price, usdt_value, date)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (mint, symbol, buy_price, sell_price, usdt_value, date)
        )
        return cursor.fetchone()['id']

def get_trading_history(history_id: int) -> Optional[TradingHistory]:
    with get_cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM trading_history 
            WHERE id = %s
            """,
            (history_id,)
        )
        data = cursor.fetchone()
        
        if data:
            return TradingHistory(
                id=data['id'],
                mint=data['mint'],
                symbol=data['symbol'],
                usdt_value=data['usdt_value'],
                buy_price=data['buy_price'],
                sell_price=data['sell_price'],
                date=data['date']
            )
        return None

def get_all_trading_history(limit: int = 100, offset: int = 0) -> List[TradingHistory]:
    with get_cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM trading_history
            ORDER BY date DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        
        return [
            TradingHistory(
                id=row['id'],
                mint=row['mint'],
                symbol=row['symbol'],
                usdt_value=row['usdt_value'],
                buy_price=row['buy_price'],
                sell_price=row['sell_price'],
                date=row['date']
            )
            for row in cursor.fetchall()
        ]

def get_trading_history_by_token(mint: str) -> List[TradingHistory]:
    with get_cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM trading_history
            WHERE mint = %s
            ORDER BY date DESC
            """,
            (mint,)
        )
        
        return [
            TradingHistory(
                id=row['id'],
                mint=row['mint'],
                symbol=row['symbol'],
                usdt_value=row['usdt_value'],
                buy_price=row['buy_price'],
                sell_price=row['sell_price'],
                date=row['date']
            )
            for row in cursor.fetchall()
        ]

def delete_trading_history(history_id: int) -> bool:
    with get_cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM trading_history
            WHERE id = %s
            """,
            (history_id,)
        )
        return cursor.rowcount > 0
