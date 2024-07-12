from Foundation import NSDate
from EventKit import EKEventStore, EKReminder, EKEntityTypeReminder

def get_reminders_from_list(list_name):
    # Create an event store
    store = EKEventStore.alloc().init()
    
    # Request access to reminders
    store.requestAccessToEntityType_completion_(EKEntityTypeReminder, None)
    
    # Get all reminder lists
    calendars = store.calendarsForEntityType_(EKEntityTypeReminder)
    
    # Find the specified list
    target_calendar = None
    for calendar in calendars:
        if calendar.title() == list_name:
            target_calendar = calendar
            break
    
    if not target_calendar:
        print(f"List '{list_name}' not found.")
        return []
    
    # Create a predicate to fetch reminders from the specified list
    predicate = store.predicateForRemindersInCalendars_([target_calendar])
    
    # Fetch reminders
    reminders = store.remindersMatchingPredicate_(predicate)
    
    return reminders

def print_reminder_details(reminder):
    print(f"Title: {reminder.title()}")
    print(f"Notes: {reminder.notes()}")
    print(f"UUID: {reminder.UUID()}")
    # print all the reminder methods
    print(f"Completed: {'Yes' if reminder.isCompleted() else 'No'}")
    if reminder.dueDate():
        print(f"Due Date: {reminder.dueDate()}")
    print("------------------------")

# Main execution
if __name__ == "__main__":
    list_name = "temp.crap"
    reminders = get_reminders_from_list(list_name)
    
    if reminders:
        print(f"Reminders in the list '{list_name}':")
        for reminder in reminders:
            print_reminder_details(reminder)
    else:
        print(f"No reminders found in the list '{list_name}'.")
