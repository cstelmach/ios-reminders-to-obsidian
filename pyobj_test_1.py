import objc
from Foundation import NSObject, NSRunLoop, NSDate
from EventKit import EKEventStore, EKEntityTypeReminder, EKReminder

class AccessDelegate(NSObject):
    def init(self):
        self = objc.super(AccessDelegate, self).init()
        if self is None: return None
        self.access_granted = False
        return self

    def requestAccessToEntityType_completion_(self, granted, error):
        self.access_granted = granted
        if error:
            print(f"Error: {error}")
        NSRunLoop.currentRunLoop().stop()

def request_access():
    store = EKEventStore.alloc().init()
    delegate = AccessDelegate.alloc().init()
    store.requestAccessToEntityType_completion_(EKEntityTypeReminder, delegate.requestAccessToEntityType_completion_)
    
    NSRunLoop.currentRunLoop().runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(10))
    return delegate.access_granted, store

def fetch_reminders(store, list_name):
    calendars = store.calendarsForEntityType_(EKEntityTypeReminder)
    calendar = None
    for cal in calendars:
        if cal.title() == list_name:
            calendar = cal
            break

    if calendar is None:
        print(f"No calendar found with name: {list_name}")
        return []

    predicate = store.predicateForRemindersInCalendars_([calendar])
    reminders = []

    def fetch_completion_handler(reminders_list):
        nonlocal reminders
        if reminders_list:
            reminders.extend(reminders_list)
        NSRunLoop.currentRunLoop().stop()

    store.fetchRemindersMatchingPredicate_completion_(predicate, fetch_completion_handler)
    NSRunLoop.currentRunLoop().runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(10))

    return reminders

if __name__ == "__main__":
    granted, store = request_access()
    if not granted:
        print("Access to reminders was denied")
    else:
        reminders = fetch_reminders(store, "temp.crap")
        for reminder in reminders:
            print(f"Reminder: {reminder.title()} - Completed: {reminder.completed()} - Due Date: {reminder.dueDateComponents()}")