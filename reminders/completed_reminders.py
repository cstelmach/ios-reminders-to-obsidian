from Foundation import NSDate
from EventKit import EKEventStore, EKEntityTypeReminder
from datetime import datetime
from database import get_tags_for_reminder, get_url_for_reminder


def get_completed_reminders_for_list(list_name, start_date=None, end_date=None):
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
            completion_date = reminder.completionDate()
            creation_date = reminder.creationDate()

            if completion_date:
                completion_date = datetime.fromtimestamp(
                    completion_date.timeIntervalSince1970()
                )
                creation_date = datetime.fromtimestamp(
                    creation_date.timeIntervalSince1970()
                )

                if (start_date is None or completion_date.date() >= start_date) and (
                    end_date is None or completion_date.date() <= end_date
                ):
                    tags = get_tags_for_reminder(reminder.calendarItemIdentifier())
                    url = get_url_for_reminder(reminder.calendarItemIdentifier())
                    completed_reminders.append(
                        {
                            "name": reminder.title(),
                            "body": reminder.notes(),
                            "creationDate": creation_date.strftime("%Y-%m-%d %H:%M:%S"),
                            "completionDate": completion_date.strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            "allDayDueDate": reminder.dueDateAllDay(),
                            "dueDate": (
                                datetime.fromtimestamp(
                                    reminder.dueDate().timeIntervalSince1970()
                                ).strftime("%Y-%m-%d %H:%M:%S")
                                if reminder.dueDate()
                                else None
                            ),
                            "priority": reminder.priority(),
                            "UUID": reminder.calendarItemIdentifier(),
                            "tags": tags,
                            "url": url,
                        }
                    )

    return completed_reminders
