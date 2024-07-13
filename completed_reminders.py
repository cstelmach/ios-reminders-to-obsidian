from Foundation import NSDate
from EventKit import EKEventStore, EKEntityTypeReminder


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
