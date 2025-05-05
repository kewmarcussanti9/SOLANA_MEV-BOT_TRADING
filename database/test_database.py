from database.connection import init_db
from database.crud.wallet import wallet_history_ops, wallet_tokens_ops
from decimal import Decimal
from global_config import WSOL

# database initialisation
#init_db()

# Example: delete wallet history
history_id = wallet_history_ops.delete_wallet_history(2)
print(f"result: {history_id}")