from dataclasses import dataclass
from typing import Optional

@dataclass
class TopMeme:
    id: Optional[int] = None
    mint: str = ""
    symbol: str = ""
