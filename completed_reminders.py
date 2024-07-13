from Foundation import NSDate
from EventKit import EKEventStore, EKEntityTypeReminder
from datetime import datetime


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
    today = datetime.now().date()

    for reminder in reminders:
        if reminder.isCompleted():
            completion_date = (
                reminder.completionDate().description()
                if reminder.completionDate()
                else None
            )
            if completion_date:
                # Parse the completion date
                completion_date_obj = datetime.strptime(
                    completion_date, "%Y-%m-%d %H:%M:%S %z"
                ).date()
                if completion_date_obj < today:
                    completed_reminders.append(
                        {
                            "name": reminder.title(),
                            "body": reminder.notes(),
                            "creationDate": reminder.creationDate().description(),
                            "completionDate": completion_date,
                            "allDayDueDate": reminder.dueDateAllDay(),
                            "dueDate": (
                                reminder.dueDate().description()
                                if reminder.dueDate()
                                else None
                            ),
                            "priority": reminder.priority(),
                            "UUID": reminder.calendarItemIdentifier(),
                            "parent_uuid": reminder.calendarItemExternalIdentifier(),
                        }
                    )

    return completed_reminders
