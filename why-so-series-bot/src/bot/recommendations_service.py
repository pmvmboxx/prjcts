from database import get_connection
import random

def get_random_series() -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM series")
    rows = cursor.fetchall()
    conn.close()
    return random.choice(rows)

def format_series(s: dict) -> str:
    """Format a series dict into a nice message string."""
    return (
        f"🎬 *{s['title']}*\n"
        f"🎭 Genre: {s['genre'].capitalize()}\n"
        f"📖 {s['description']}\n"
        f"⭐ IMDb: {s['rating']}"
    )