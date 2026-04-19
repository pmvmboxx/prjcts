import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / 'database.db'

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS series (
            series_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            genre TEXT,
            year INTEGER,
            poster_url TEXT,
            tmdb_id INTEGER,
            rating REAL
        );

        CREATE TABLE IF NOT EXISTS episodes (
            episode_id INTEGER PRIMARY KEY AUTOINCREMENT,
            series_id INTEGER NOT NULL,
            season_number INTEGER,
            episode_number INTEGER,
            title TEXT,
            level TEXT,
            justwatch_url TEXT,
            opensubtitles_id TEXT,
            FOREIGN KEY (series_id) REFERENCES series(series_id)
        );

        CREATE TABLE IF NOT EXISTS posts (
            post_id INTEGER PRIMARY KEY AUTOINCREMENT,
            episode_id INTEGER NOT NULL UNIQUE,
            quote TEXT,
            quote_speaker TEXT,
            quizlet_url TEXT,
            practice_url TEXT,
            vocab TEXT,
            idioms TEXT,
            status TEXT DEFAULT 'draft',
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (episode_id) REFERENCES episodes(episode_id)
        );

        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id TEXT NOT NULL UNIQUE,
            first_name TEXT,
            username TEXT,
            joined_at TEXT DEFAULT (datetime('now')),
            is_admin INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS user_library (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            series_id INTEGER NOT NULL,
            status TEXT DEFAULT 'nothing',
            added_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (series_id) REFERENCES series(series_id),
            UNIQUE(user_id, series_id)
        );

        CREATE TABLE IF NOT EXISTS user_episode_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            episode_id INTEGER NOT NULL,
            practised INTEGER DEFAULT 0,
            practised_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (episode_id) REFERENCES episodes(episode_id),
            UNIQUE(user_id, episode_id)
        );

        CREATE TABLE IF NOT EXISTS user_posts (
            user_post_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            series_title TEXT,
            season_number INTEGER,
            episode_number INTEGER,
            quote TEXT,
            quote_speaker TEXT,
            quizlet_url TEXT,
            practice_url TEXT,
            vocab TEXT,
            idioms TEXT,
            status TEXT DEFAULT 'private',
            linked_episode_id INTEGER,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (linked_episode_id) REFERENCES episodes(episode_id)
        );
    """)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully")