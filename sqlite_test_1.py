import sqlite3

def find_parent_reminder(reminder_uuid):
    # Path to the Reminders SQLite database
    db_path = "/Users/cs/Library/Group Containers/group.com.apple.reminders/Container_v1/Stores/Data-FEC9D2EC-9C03-4EE5-A85C-AD1172799AC7.sqlite"

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to find the parent reminder UUID
        query = """
        SELECT ZPARENTREMINDER.ZCKIDENTIFIER as parent_uuid
        FROM ZREMCDREMINDER as CHILD
        JOIN ZREMCDREMINDER as ZPARENTREMINDER ON CHILD.ZCKPARENTREMINDERIDENTIFIER = ZPARENTREMINDER.ZCKIDENTIFIER
        WHERE CHILD.ZCKIDENTIFIER = ?
        """

        cursor.execute(query, (reminder_uuid,))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return "No parent reminder found or the reminder is not a subtask."

    except sqlite3.Error as e:
        return f"An error occurred: {e}"

    finally:
        if conn:
            conn.close()

# Example usage
reminder_uuid = "2DE026DC-F783-4512-8114-C2D03D9A90BE"
parent_uuid = find_parent_reminder(reminder_uuid)
print(f"The parent reminder UUID for {reminder_uuid} is: {parent_uuid}")

# example 2 "57161380-3310-41D5-ADEA-99E4B6A4DF9F"
reminder_uuid = "57161380-3310-41D5-ADEA-99E4B6A4DF9F"
parent_uuid = find_parent_reminder(reminder_uuid)
print(f"The parent reminder UUID for {reminder_uuid} is: {parent_uuid}")