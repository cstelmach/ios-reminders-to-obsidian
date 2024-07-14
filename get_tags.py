import sqlite3
import os
import glob

def get_tags_from_db():
    db_glob_path = os.path.expanduser(
        "~/Library/Group Containers/group.com.apple.reminders/Container_v1/Stores/Data-*.sqlite"
    )
    db_paths = glob.glob(db_glob_path)

    if not db_paths:
        raise FileNotFoundError("No SQLite database found for Reminders.")

    db_paths.sort(key=lambda x: os.path.getsize(x), reverse=True)
    db_path = db_paths[0]

    conn = None
    tags = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = """
        SELECT ZNAME
        FROM ZREMCDHASHTAGLABEL
        """
        cursor.execute(query)
        results = cursor.fetchall()
        tags = [row[0] for row in results]
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
    return tags

if __name__ == "__main__":
    tags = get_tags_from_db()
    print("Available tags:", tags)