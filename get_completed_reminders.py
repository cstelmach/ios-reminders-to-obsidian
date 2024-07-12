import sqlite3
import json
import os
import glob
import sys

def get_completed_reminders(list_name):
    db_path = os.path.expanduser("~/Library/Group Containers/group.com.apple.reminders/Container_v1/Stores/Data-*.sqlite")
    db_files = glob.glob(db_path)
    
    if not db_files:
        return json.dumps({"error": "Reminders database not found"})

    db_file = db_files[0]  # Use the first matching database file

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    query = """
    SELECT 
        r.Z_PK,
        r.ZTITLE,
        r.ZNOTES,
        r.ZCREATIONDATE,
        r.ZCOMPLETIONDATE,
        r.ZDUEDATE,
        r.ZPRIORITY,
        p.Z_PK as parent_id,
        p.ZTITLE as parent_title
    FROM ZREMCDREMINDER r
    LEFT JOIN ZREMCDREMINDER p ON r.ZCKPARENTREMINDERIDENTIFIER = p.ZCKIDENTIFIER
    JOIN ZREMCDOBJECT o ON r.Z_PK = o.ZREMINDER
    JOIN ZREMCDOBJECT l ON o.Z_FOK_PARENTLIST1 = l.Z_PK
    WHERE l.ZNAME2 = ? AND r.ZCOMPLETED = 1
    """

    cursor.execute(query, (list_name,))
    reminders = cursor.fetchall()

    conn.close()

    result = []
    for row in reminders:
        reminder = {
            "id": row[0],
            "title": row[1],
            "notes": row[2],
            "creation_date": row[3],
            "completion_date": row[4],
            "due_date": row[5],
            "priority": row[6],
            "parent_reminder": {
                "id": row[7],
                "title": row[8]
            } if row[7] else None
        }
        result.append(reminder)

    return json.dumps(result)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a list name as an argument.")
        # sys.exit(1)
    # list_name = sys.argv[1]
    # print(get_completed_reminders(list_name))
    print(get_completed_reminders("temp.crap"))