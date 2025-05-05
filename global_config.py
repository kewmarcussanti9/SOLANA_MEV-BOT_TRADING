from dotenv import load_dotenv
import os

# Load variables from .env into environment
load_dotenv()

# WALLETS ADDRESS
WALLET_PUB_KEY = os.getenv("PUBLIC_KEY")
WALLET_PRIV_KEY = os.getenv("PRIVATE_KEY")

# URLS
HELIUS_RPC = f"https://mainnet.helius-rpc.com/?api-key={os.getenv('HELIUS_API_KEY')}"
SOL_URI = 'https://api.mainnet-beta.solana.com'     # "https://api.devnet.solana.com"
SOL_WSS = 'wss://api.mainnet-beta.solana.com'       # "wss://api.devnet.solana.com"

# Common Token Mint Addresses
WSOL = 'So11111111111111111111111111111111111111112'
USDT = 'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB'
USDC = 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'
