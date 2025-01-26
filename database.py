import sqlite3

DB_NAME = "tasks.db"


def initialize():
    """Create table if dont exist"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,            -- Task name
                description TEXT,               -- Optional description
                created_at TEXT DEFAULT CURRENT_TIMESTAMP -- Task creation timestamp
            );


            CREATE TABLE IF NOT EXISTS tracking_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,       -- Links to the task being tracked
                start_time TEXT NOT NULL,       -- When tracking started
                end_time TEXT,                  -- When tracking ended
                duration INTEGER,               -- Automatically calculated (seconds)
                FOREIGN KEY (task_id) REFERENCES tasks (id)
            );

            CREATE TABLE IF NOT EXISTS days (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL UNIQUE,      -- YYYY-MM-DD format
                total_duration INTEGER DEFAULT 0 -- Total seconds spent on all tasks that day
            );

              """)
        conn.commit()
     

if __name__ == "__main__":
    initialize()
    print("Dtabase has been initialized.")
