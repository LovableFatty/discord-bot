import sqlite3

# Initialize database connection
db_conn = sqlite3.connect("bot_data.db")
db_cursor = db_conn.cursor()


def init_db():
    db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS balances (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER DEFAULT 0
        )
    """)
    db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS quests (
            quest_id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            reward INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'open',
            player_id INTEGER DEFAULT NULL
        )
    """)
    db_conn.commit()
