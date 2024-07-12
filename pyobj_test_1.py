import objc
from Foundation import NSObject, NSRunLoop, NSDate
from EventKit import EKEventStore, EKReminder, EKEntityType

# Initialize Event Store
store = EKEventStore.alloc().init()

# Request access to Reminders
def request_access():
    granted = store.requestAccessToEntityType_error_(EKEntityTypeReminder, None)
    if granted:
        print("Access to Reminders granted.")
    else:
        print("Access to Reminders denied.")
    return granted

# Check access
if not request_access():
    exit("Permission not granted.")

# Define a function to get all completed reminders
def get_completed_reminders():
    # Set the time range for the search (past year)
    end_date = NSDate.date()
    start_date = end_date.dateByAddingTimeInterval_(-365 * 24 * 60 * 60)  # One year ago

    # Create predicate to search for reminders within the time range
    predicate = store.predicateForRemindersInCalendars_(None)

    # Temporary list to hold completed reminders
    temp_crap = []

    # Fetch reminders
    def fetch_reminders(reminders_list):
        for reminder in reminders_list:
            if reminder.completed():
                temp_crap.append({
                    'title': reminder.title(),
                    'due_date': reminder.dueDateComponents(),
                    'completion_date': reminder.completionDate()
                })

    store.fetchRemindersMatchingPredicate_completion(predicate, fetch_reminders)

    # Run the run loop to allow asynchronous operations to complete
    NSRunLoop.currentRunLoop().runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(5))

    return temp_crap

# Fetch completed reminders into the temp.crap list
temp = {'crap': get_completed_reminders()}

# Print completed reminders
for reminder in temp['crap']:
    title = reminder['title']
    due_date = reminder['due_date']
    completion_date = reminder['completion_date']
    print(f"Title: {title}")
    if due_date:
        print(f"Due Date: {due_date}")
    if completion_date:
        print(f"Completion Date: {completion_date}")
    print()
