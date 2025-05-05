import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from .config import DATABASE_URL


def get_connection():
    """Connect to the database"""
    return psycopg2.connect(DATABASE_URL)

@contextmanager
def get_cursor(cursor_factory=RealDictCursor):
    """Obtain a cursor and manage the connection
    Args: cursor_factory: default 'RealDictCursor' to returns results as dictionaries."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=cursor_factory)
        yield cursor
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def init_db():
    """Initialize the database with the required tables."""
    with get_cursor() as cursor:
        # Wallet History
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallet_history (
            id SERIAL PRIMARY KEY,
            date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            balance_usdt DECIMAL(20, 8) NOT NULL,
            balance_sol DECIMAL(20, 8) NOT NULL
        )
        """)
        
        # Wallet Tokens
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS wallet_token (
            id SERIAL PRIMARY KEY,
            mint VARCHAR(255) NOT NULL UNIQUE,
            symbol VARCHAR(50),
            purchase_price DECIMAL(20, 8),
            usdt_value DECIMAL(20, 8) NOT NULL
        )
        """)
        
        # Tokens Trading History
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS trading_history (
            id SERIAL PRIMARY KEY,
            mint VARCHAR(255) NOT NULL,
            symbol VARCHAR(50),
            buy_price DECIMAL(20, 8)  NOT NULL,
            sell_price DECIMAL(20, 8)  NOT NULL,
            usdt_value DECIMAL(20, 8) NOT NULL,
            date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Top Memes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS top_meme (
            id SERIAL PRIMARY KEY,
            mint VARCHAR(255) NOT NULL UNIQUE,
            symbol VARCHAR(50) NOT NULL
        )
        """)
        
        print(">> Base de données initialisée avec succès!")
