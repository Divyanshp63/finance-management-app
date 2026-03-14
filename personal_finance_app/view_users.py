import sqlite3
import os

# Path to your database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "finance.db")

def view_users():
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        return

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query all rows from the User table
        cursor.execute("SELECT id, username, email, full_name, phone FROM user")
        rows = cursor.fetchall()

        if not rows:
            print("No users found in the database.")
        else:
            print("-" * 100)
            print(f"{'ID':<4} | {'Username':<15} | {'Email':<30} | {'Full Name':<20} | {'Phone':<15}")
            print("-" * 100)
            for row in rows:
                id_val, uname, email, fname, phone = row
                print(f"{id_val:<4} | {uname:<15} | {email:<30} | {str(fname):<20} | {str(phone):<15}")
            print("-" * 100)

        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    view_users()
