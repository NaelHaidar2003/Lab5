import sqlite3

def connect_to_db():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect('database.db')
    return conn

def create_db_table():
    """Create the users table if it doesn't exist."""
    try:
        conn = connect_to_db()
        conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            country TEXT NOT NULL
        );
        ''')
        conn.commit()
    except Exception as e:
        print(f"Error creating user table: {e}")
    finally:
        conn.close()

def insert_user(user):
    """Insert a new user into the users table."""
    inserted_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)", 
                    (user['name'], user['email'], user['phone'], user['address'], user['country']))
        conn.commit()
        
        if cur.lastrowid:
            inserted_user = get_user_by_id(cur.lastrowid)
    except Exception as e:
        print(f"Error inserting user: {e}")
        conn.rollback()
    finally:
        conn.close()
    return inserted_user

def get_users():
    """Fetch all users from the users table."""
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        for row in rows:
            user = {
                "user_id": row["user_id"],
                "name": row["name"],
                "email": row["email"],
                "phone": row["phone"],
                "address": row["address"],
                "country": row["country"]
            }
            users.append(user)
    except Exception as e:
        print(f"Error fetching users: {e}")
    finally:
        conn.close()
    return users

def get_user_by_id(user_id):
    """Fetch a user by their user_id."""
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        if row:
            user = {
                "user_id": row["user_id"],
                "name": row["name"],
                "email": row["email"],
                "phone": row["phone"],
                "address": row["address"],
                "country": row["country"]
            }
    except Exception as e:
        print(f"Error fetching user by ID: {e}")
    finally:
        conn.close()
    return user

def update_user(user):
    """Update a user's details."""
    updated_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ? WHERE user_id = ?",
                    (user["name"], user["email"], user["phone"], user["address"], user["country"], user["user_id"]))
        conn.commit()
        updated_user = get_user_by_id(user["user_id"])
    except Exception as e:
        print(f"Error updating user: {e}")
        conn.rollback()
    finally:
        conn.close()
    return updated_user

def delete_user(user_id):
    """Delete a user by their user_id."""
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except Exception as e:
        print(f"Error deleting user: {e}")
        conn.rollback()
        message["status"] = "Cannot delete user"
    finally:
        conn.close()
    return message
