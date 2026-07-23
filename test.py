from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT id, name, email FROM users")

users = cursor.fetchall()

print(users)

conn.close()