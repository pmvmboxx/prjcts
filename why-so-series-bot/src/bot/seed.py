from database import get_connection
import sqlite3

def seed_database():
    # 1. Connect to the database
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Optional: Clear existing data to avoid UNIQUE constraint errors during testing
        cursor.execute("DELETE FROM user_episode_progress")
        cursor.execute("DELETE FROM user_library")
        cursor.execute("DELETE FROM user_posts")
        cursor.execute("DELETE FROM posts")
        cursor.execute("DELETE FROM episodes")
        cursor.execute("DELETE FROM series")
        cursor.execute("DELETE FROM users")

        print("--- Seeding Series ---")
        series_data = [
            ("Breaking Bad", "Crime, Drama", 2008, 9.5, "A high school chemistry teacher turned drug kingpin."),
            ("The Bear", "Comedy, Drama", 2022, 8.6, "A young chef returns to Chicago to run his family sandwich shop.")
        ]
        series_ids = {}
        
        for s in series_data:
            cursor.execute("""
                INSERT INTO series (title, genre, year, rating, description)
                VALUES (?, ?, ?, ?, ?)
            """, s)
            series_ids[s[0]] = cursor.lastrowid  # store ID by title
        # Get the series_id for Breaking Bad (the first one inserted)
        
        bb_id = series_ids["Breaking Bad"]
        bear_id = series_ids["The Bear"]

        print("--- Seeding Episodes ---")
        episodes_data = [
            (bb_id, 1, 1, "Pilot", "B1", "https://justwatch.com/bb-p1", "os-123"),
            (bb_id, 1, 2, "Cat's in the Bag...", "B1", "https://justwatch.com/bb-p2", "os-124")
        ]
        
        for e in episodes_data:
            cursor.execute("""
                INSERT INTO episodes (series_id, season_number, episode_number, title, level, justwatch_url, opensubtitles_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, e)
        
        # Get the episode_id for the Pilot
        pilot_id = cursor.lastrowid

        print("--- Seeding Posts (Study Material) ---")
        cursor.execute("""
            INSERT INTO posts (episode_id, quote, quote_speaker, vocab, idioms, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (pilot_id, "I am the one who knocks!", "Walter White", "Chemistry, Lung Cancer", "Break a leg", "published"))

        print("--- Seeding Users ---")
        cursor.execute("""
            INSERT INTO users (telegram_id, first_name, username, is_admin)
            VALUES (?, ?, ?, ?)
        """, ("55882211", "Jesse", "pinkman_capn", 0))
        
        user_id = cursor.lastrowid

        print("--- Seeding User Library & Progress ---")
        # Add Breaking Bad to Jesse's library
        cursor.execute("""
            INSERT INTO user_library (user_id, series_id, status)
            VALUES (?, ?, ?)
        """, (user_id, bb_id, "in_progress"))

        # Mark Pilot as practiced
        cursor.execute("""
            INSERT INTO user_episode_progress (user_id, episode_id, practised, practised_at)
            VALUES (?, ?, ?, datetime('now'))
        """, (user_id, pilot_id, 1))

        conn.commit()
        print("\nDatabase seeded successfully!")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    seed_database()