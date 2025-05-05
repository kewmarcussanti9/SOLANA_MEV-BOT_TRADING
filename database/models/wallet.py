from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

@dataclass
class WalletHistory:
    id: Optional[int] = None
    date: datetime = None
    balance_usdt: Decimal = Decimal('0')
    balance_sol: Decimal = Decimal('0')
    
    def __post_init__(self):
        if self.date is None:
            self.date = datetime.now()

@dataclass
class WalletToken:
    id: Optional[int] = None
    mint: str = ""
    symbol: str = ""
    purchase_price: Optional[Decimal] = None
    usdt_value: Decimal = Decimal('0')

@dataclass
class TradingHistory:
    id: Optional[int] = None
    mint: str = ""
    symbol: str = ""
    buy_price: Optional[Decimal] = None
    sell_price: Optional[Decimal] = None
    usdt_value: Decimal = Decimal('0')
    date: datetime = None
    
    def __post_init__(self):
        if self.date is None:
            self.date = datetime.now()
