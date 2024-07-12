# ios_reminders_to_markdown_journal/reminders.py

from Foundation import NSDate
from EventKit import EKEventStore, EKReminder, EKEntityTypeReminder
import sqlite3

def get_all_reminder_lists():
    store = EKEventStore.alloc().init()
    store.requestAccessToEntityType_completion_(EKEntityTypeReminder, None)
    calendars = store.calendarsForEntityType_(EKEntityTypeReminder)
    
    reminder_lists = []
    for calendar in calendars:
        reminder_lists.append({
            'title': calendar.title(),
            'color': calendar.color(),
            'type': calendar.type(),
            'allowsContentModifications': calendar.allowsContentModifications(),
            'UUID': str(calendar.calendarIdentifier())
        })
    return reminder_lists

def get_completed_reminders_for_list(list_name):
    store = EKEventStore.alloc().init()
    store.requestAccessToEntityType_completion_(EKEntityTypeReminder, None)
    calendars = store.calendarsForEntityType_(EKEntityTypeReminder)
    
    target_calendar = next((calendar for calendar in calendars if calendar.title() == list_name), None)
    if not target_calendar:
        print(f"List '{list_name}' not found.")
        return []
    
    predicate = store.predicateForRemindersInCalendars_([target_calendar])
    reminders = store.remindersMatchingPredicate_(predicate)
    
    completed_reminders = []
    for reminder in reminders:
        if reminder.isCompleted():
            completed_reminders.append({
                'name': reminder.title(),
                'body': reminder.notes(),
                'creationDate': reminder.creationDate().description(),
                'completionDate': reminder.completionDate().description() if reminder.completionDate() else None,
                'allDayDueDate': reminder.dueDateAllDay(),
                'dueDate': reminder.dueDate().description() if reminder.dueDate() else None,
                'priority': reminder.priority(),
                'UUID': reminder.UUID()
            })
    
    return completed_reminders

def find_parent_reminder(reminder_uuid):
    db_path = "/Users/cs/Library/Group Containers/group.com.apple.reminders/Container_v1/Stores/Data-FEC9D2EC-9C03-4EE5-A85C-AD1172799AC7.sqlite"
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
            return {'uuid': result[0], 'title': result[1]}
        else:
            return None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if conn:
            conn.close()