from database import get_connection
import sqlite3

def seed_database():
    # 1. Connect to the database
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # to avoid UNIQUE/Foreign Key conflicts
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
            ("The Bear", "Comedy, Drama", 2022, 8.6, "A young chef returns to Chicago to run his family sandwich shop."),
            ("Friends", "Comedy, Romance", 1994, 8.9, "Six 20-something friends live in Manhattan."),
            ("Stranger Things", "Sci-Fi, Horror", 2016, 8.7, "A group of kids uncover government secrets in the 80s."),
            ("Succession", "Drama", 2018, 8.9, "A family fights for control of a global media empire."),
            ("Wednesday", "Fantasy, Mystery", 2022, 8.1, "Wednesday Addams investigates a murder spree."),
            ("Ted Lasso", "Comedy, Sports", 2020, 8.8, "An American football coach moves to England."),
            ("The Office", "Comedy", 2005, 9.0, "Dunder Mifflin employees navigate office life.")
        ]
        
        series_ids = {}
        for s in series_data:
            cursor.execute("""
                INSERT INTO series (title, genre, year, rating, description)
                VALUES (?, ?, ?, ?, ?)
            """, s)
            series_ids[s[0]] = cursor.lastrowid 
        
        bb_id = series_ids["Breaking Bad"]
        friends_id = series_ids["Friends"]

        print("--- Seeding Episodes ---")

        cursor.execute("""
            INSERT INTO episodes (series_id, season_number, episode_number, title, level, justwatch_url, opensubtitles_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (bb_id, 1, 1, "Pilot", "B1", "https://justwatch.com/bb-p1", "os-123"))
        pilot_id = cursor.lastrowid


        other_episodes = [
            (bb_id, 1, 2, "Cat's in the Bag...", "B1", "https://justwatch.com/bb-p2", "os-124"),
            (friends_id, 1, 1, "The One Where Monica Gets a Roommate", "A2", "https://justwatch.com/f-p1", "os-999")
        ]
        for e in other_episodes:
            cursor.execute("""
                INSERT INTO episodes (series_id, season_number, episode_number, title, level, justwatch_url, opensubtitles_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, e)

        print("--- Seeding Posts (Study Material) ---")
        cursor.execute("""
            INSERT INTO posts (episode_id, quote, quote_speaker, vocab, idioms, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (pilot_id, "I am the one who knocks!", "Walter White", "Chemistry, Lung Cancer", "Break a leg", "published"))

        print("--- Seeding User ---")
        cursor.execute("""
            INSERT INTO users (telegram_id, first_name, username, is_admin)
            VALUES (?, ?, ?, ?)
        """, ("55882211", "Jesse", "pinkman_capn", 0))
        user_id = cursor.lastrowid

        print("--- Seeding User Library & Progress ---")
        cursor.execute("""
            INSERT INTO user_library (user_id, series_id, status)
            VALUES (?, ?, ?)
        """, (user_id, bb_id, "in_progress"))

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