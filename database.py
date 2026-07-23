import sqlite3
DATABASE_NAME = "prediction_history.db"

def get_connection():
    return sqlite3.connect(DATABASE_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Predictions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,

        model_year INTEGER NOT NULL,
        make TEXT NOT NULL,
        vehicle_class TEXT NOT NULL,

        engine_size REAL NOT NULL,
        cylinders INTEGER NOT NULL,

        transmission TEXT NOT NULL,
        fuel_type TEXT NOT NULL,

        fuel_consumption REAL NOT NULL,

        predicted_co2 REAL NOT NULL,

        eco_score REAL,

        confidence_score REAL,
        confidence_level TEXT,

        prediction_lower REAL,
        prediction_upper REAL,

        top_influencing_feature TEXT,

        recommendations TEXT,

        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()



