# reminder_tags.py
from ios_reminders_to_markdown_journal.database.db_utils import get_db_connection


def get_tags_for_reminder(reminder_uuid):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = """
        SELECT LABEL.ZNAME 
        FROM ZREMCDOBJECT as OBJ 
        JOIN ZREMCDREMINDER as REM ON OBJ.ZREMINDER3 = REM.Z_PK 
        JOIN ZREMCDHASHTAGLABEL as LABEL ON OBJ.ZNAME1 = LABEL.ZNAME 
        WHERE REM.ZCKIDENTIFIER = ?
        """
        cursor.execute(query, (reminder_uuid,))
        results = cursor.fetchall()
        return [row[0] for row in results]
    finally:
        conn.close()


if __name__ == "__main__":
    reminder_uuid = input("Enter the reminder UUID: ")
    tags = get_tags_for_reminder(reminder_uuid)
    print(f"Tags for reminder {reminder_uuid}: {tags}")
