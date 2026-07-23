import bcrypt
from database import get_connection

def hash_password(password):
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(password, hashed_password):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

def signup_user(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if email already exists
    cursor.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    )

    if cursor.fetchone():
        conn.close()
        return False, "Email already exists."

    # Hash the password
    hashed_password = hash_password(password)

    # Insert the new user
    cursor.execute("""
        INSERT INTO users (name, email, password_hash)
        VALUES (?, ?, ?)
    """, (name, email, hashed_password))

    conn.commit()
    conn.close()

    return True, "Account created successfully."

def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, password_hash
        FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    conn.close()

    if user is None:
        return False, "Email not found."

    user_id, name, email, password_hash = user

    if verify_password(password, password_hash):
        return True, {
            "id": user_id,
            "name": name,
            "email": email
        }

    return False, "Incorrect password."