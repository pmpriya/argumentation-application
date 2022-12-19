import sqlite3

try:
    conn = sqlite3.connect('argupedia_database.db')
    cursor = conn.execute("SELECT * from argument_table")
    conn.close()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if conn:
        conn.close()
        print("The SQLite connection is closed")

