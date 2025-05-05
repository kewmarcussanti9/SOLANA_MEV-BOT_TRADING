from decimal import Decimal
from datetime import datetime
from database.connection import get_cursor
from database.models.wallet import WalletHistory


def create_wallet_history(balance_usdt: Decimal, balance_sol: Decimal, date: datetime = None) -> int:
    """
    Adds a new entry to the wallet history.

    Args:
        balance_usdt: USDT wallet balance
        balance_sol: Solana wallet balance
        date: Entry date (default: now)

    Returns:
        int: ID of the newly created entry
    """
    if date is None:
        date = datetime.now()
        
    with get_cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO wallet_history (date, balance_usdt, balance_sol)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (date, balance_usdt, balance_sol)
        )
        return cursor.fetchone()['id']

def get_wallet_history(history_id: int) -> WalletHistory:
    """
    Retrieves a specific wallet history entry by its ID.
    Args:
        history_id: ID of the wallet history entry
    Returns:
        WalletHistory: The wallet history entry
    """
    with get_cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM wallet_history 
            WHERE id = %s
            """,
            (history_id,)
        )
        data = cursor.fetchone()
        
        if data:
            return WalletHistory(
                id=data['id'],
                date=data['date'],
                balance_usdt=data['balance_usdt'],
                balance_sol=data['balance_sol']
            )
        return None

def delete_wallet_history(history_id: int) -> bool:
    with get_cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM wallet_history
            WHERE id = %s
            """,
            (history_id,)
        )
        return cursor.rowcount > 0

def get_all_wallet_history(limit: int = 100, offset: int = 0):
    """
    Retrieves all wallet history entries.
    Args:
        limit: Number of entries to retrieve
        offset: Number of entries to skip
    Returns:
        list[WalletHistory]: List of wallet history entries
    """
    with get_cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM wallet_history
            ORDER BY date DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        
        return [
            WalletHistory(
                id=row['id'],
                date=row['date'],
                balance_usdt=row['balance_usdt'],
                balance_sol=row['balance_sol']
            )
            for row in cursor.fetchall()
        ]

def get_latest_wallet_history() -> WalletHistory:
    with get_cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM wallet_history
            ORDER BY date DESC
            LIMIT 1
            """
        )
        data = cursor.fetchone()
        
        if data:
            return WalletHistory(
                id=data['id'],
                date=data['date'],
                balance_usdt=data['balance_usdt'],
                balance_sol=data['balance_sol']
            )
        return None

def get_wallet_history_by_date_range(start_date: datetime, end_date: datetime):
    """
    Retrieves wallet history entries within a specific date range.
    Args:
        start_date: Start date of the range
        end_date: End date of the range
    Returns:
        list[WalletHistory]: List of wallet history entries
    """
    with get_cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM wallet_history 
            WHERE date BETWEEN %s AND %s
            """,
            (start_date, end_date)
        )
        
        return [
            WalletHistory(
                id=row['id'],
                date=row['date'],
                balance_usdt=row['balance_usdt'],
                balance_sol=row['balance_sol']
            )
            for row in cursor.fetchall()
        ]
