from database import get_db_connection


def find_parent_reminder(reminder_uuid):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = """
        SELECT ZPARENTREMINDER.ZCKIDENTIFIER as parent_uuid, ZPARENTREMINDER.ZTITLE as parent_title
        FROM ZREMCDREMINDER as CHILD
        JOIN ZREMCDREMINDER as ZPARENTREMINDER ON CHILD.ZCKPARENTREMINDERIDENTIFIER = ZPARENTREMINDER.ZCKIDENTIFIER
        WHERE CHILD.ZCKIDENTIFIER = ?
        """
        cursor.execute(query, (reminder_uuid,))
        result = cursor.fetchone()
        if result:
            return {"uuid": result[0], "title": result[1]}
        else:
            return None
    finally:
        conn.close()
