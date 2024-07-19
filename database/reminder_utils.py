from .db_utils import get_db_connection


def get_all_tags():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = "SELECT ZNAME FROM ZREMCDHASHTAGLABEL"
        cursor.execute(query)
        results = cursor.fetchall()
        return [row[0] for row in results]
    finally:
        conn.close()


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


def get_url_for_reminder(reminder_uuid):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = """
        SELECT OBJ.ZURL 
        FROM ZREMCDOBJECT as OBJ 
        JOIN ZREMCDREMINDER as REM ON OBJ.ZREMINDER2 = REM.Z_PK 
        WHERE REM.ZCKIDENTIFIER = ?
        """
        cursor.execute(query, (reminder_uuid,))
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        conn.close()


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
