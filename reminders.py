from Foundation import NSDate
from EventKit import EKEventStore, EKReminder, EKEntityTypeReminder
import os
import json
import glob
import sqlite3

def get_all_reminder_lists():
    store = EKEventStore.alloc().init()
    store.requestAccessToEntityType_completion_(EKEntityTypeReminder, None)
    calendars = store.calendarsForEntityType_(EKEntityTypeReminder)

    reminder_lists = []
    for calendar in calendars:
        reminder_lists.append(
            {
                "title": calendar.title(),
                "color": calendar.color(),
                "type": calendar.type(),
                "allowsContentModifications": calendar.allowsContentModifications(),
                "UUID": str(calendar.calendarIdentifier()),
            }
        )
    return reminder_lists

def get_completed_reminders_for_list(list_name):
    store = EKEventStore.alloc().init()
    store.requestAccessToEntityType_completion_(EKEntityTypeReminder, None)
    calendars = store.calendarsForEntityType_(EKEntityTypeReminder)

    target_calendar = next(
        (calendar for calendar in calendars if calendar.title() == list_name), None
    )
    if not target_calendar:
        print(f"List '{list_name}' not found.")
        return []

    predicate = store.predicateForRemindersInCalendars_([target_calendar])
    reminders = store.remindersMatchingPredicate_(predicate)

    completed_reminders = []
    for reminder in reminders:
        if reminder.isCompleted():
            completed_reminders.append(
                {
                    "name": reminder.title(),
                    "body": reminder.notes(),
                    "creationDate": reminder.creationDate().description(),
                    "completionDate": (
                        reminder.completionDate().description()
                        if reminder.completionDate()
                        else None
                    ),
                    "allDayDueDate": reminder.dueDateAllDay(),
                    "dueDate": (
                        reminder.dueDate().description() if reminder.dueDate() else None
                    ),
                    "priority": reminder.priority(),
                    "UUID": reminder.calendarItemIdentifier(),
                }
            )

    return completed_reminders

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
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if conn:
            conn.close()