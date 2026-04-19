import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent.parent / '.env')

BOT_TOKEN = os.getenv("BOT_TOKEN")
