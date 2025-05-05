from typing import List
from database.connection import get_cursor
from database.models.coins import TopMeme

def insert_top_meme(mint: str, symbol: str) -> int:
    with get_cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO top_meme (mint, symbol)
            VALUES (%s, %s)
            RETURNING id
            """,
            (mint, symbol)
        )
        return cursor.fetchone()['id']

def get_all_top_memes(limit: int = 100, offset: int = 0) -> List[TopMeme]:
    with get_cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM top_meme
            ORDER BY market_cap DESC NULLS LAST
            LIMIT %s OFFSET %s
            """,
            (limit, offset)
        )
        
        return [
            TopMeme(
                id=row['id'],
                mint=row['mint'],
                symbol=row['symbol'],
            )
            for row in cursor.fetchall()
        ]

def delete_top_meme(mint: str) -> None:
    with get_cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM top_meme
            WHERE mint = %s
            """,
            (mint,)
        )
