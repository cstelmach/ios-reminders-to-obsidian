import os
import glob
import sqlite3


def find_parent_reminder(reminder_uuid):
    db_glob_path = os.path.expanduser(
        "~/Library/Group Containers/group.com.apple.reminders/Container_v1/Stores/Data-*.sqlite"
    )
    db_paths = glob.glob(db_glob_path)

    if not db_paths:
        return None

    db_paths.sort(key=lambda x: os.path.getsize(x), reverse=True)
    db_path = db_paths[0]

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = """
        SELECT ZPARENTREMINDER.ZCKIDENTIFIER as parent_uuid, ZPARENTREMINDER.ZTITLE as parent_title, ZPARENTREMINDER.ZCOMPLETIONDATE as parent_completion_date
        FROM ZREMCDREMINDER as CHILD
        JOIN ZREMCDREMINDER as ZPARENTREMINDER ON CHILD.ZCKPARENTREMINDERIDENTIFIER = ZPARENTREMINDER.ZCKIDENTIFIER
        WHERE CHILD.ZCKIDENTIFIER = ?
        """
        cursor.execute(query, (reminder_uuid,))
        result = cursor.fetchone()
        if result:
            return {"uuid": result[0], "title": result[1], "completion_date": result[2]}
        else:
            return None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if conn:
            conn.close()
