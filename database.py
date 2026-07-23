import sqlite3

DATABASE_NAME = "prediction_history.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- Users Table ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ---------------- Predictions Table ----------------
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


# =====================================================
# Save Prediction
# =====================================================

def save_prediction(
    user_id,
    model_year,
    make,
    vehicle_class,
    engine_size,
    cylinders,
    transmission,
    fuel_type,
    fuel_consumption,
    predicted_co2,
    eco_score=None,
    confidence_score=None,
    confidence_level=None,
    prediction_lower=None,
    prediction_upper=None,
    top_influencing_feature=None,
    recommendations=None
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions(
            user_id,
            model_year,
            make,
            vehicle_class,
            engine_size,
            cylinders,
            transmission,
            fuel_type,
            fuel_consumption,
            predicted_co2,
            eco_score,
            confidence_score,
            confidence_level,
            prediction_lower,
            prediction_upper,
            top_influencing_feature,
            recommendations
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        model_year,
        make,
        vehicle_class,
        engine_size,
        cylinders,
        transmission,
        fuel_type,
        fuel_consumption,
        predicted_co2,
        eco_score,
        confidence_score,
        confidence_level,
        prediction_lower,
        prediction_upper,
        top_influencing_feature,
        recommendations
    ))

    conn.commit()
    conn.close()


# =====================================================
# Get All Predictions of a User
# =====================================================

def get_user_predictions(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM predictions
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


# =====================================================
# Delete a Prediction (Optional)
# =====================================================

def delete_prediction(prediction_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM predictions WHERE id = ?",
        (prediction_id,)
    )

    conn.commit()
    conn.close()