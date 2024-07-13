from Foundation import NSDate
from EventKit import EKEventStore, EKEntityTypeReminder

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