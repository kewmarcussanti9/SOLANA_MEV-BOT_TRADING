import os
from dotenv import load_dotenv
from urllib.parse import urlparse


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def parse_db_url():
    """Parse la chaîne de connexion PostgreSQL pour extraire les composants."""
    parsed = urlparse(DATABASE_URL)
    return {
        'host': parsed.hostname,
        'port': parsed.port or '5432',
        'user': parsed.username,
        'password': parsed.password,
        'database': parsed.path[1:] if parsed.path else 'neondb'
    }

# Parse the database URL and store the configuration in a dictionary
DB_CONFIG = parse_db_url()
