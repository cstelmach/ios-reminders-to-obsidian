from Foundation import NSDate
from EventKit import EKEventStore, EKEntityTypeReminder

def get_all_reminder_lists():
    # Create an event store
    store = EKEventStore.alloc().init()
    
    # Request access to reminders
    store.requestAccessToEntityType_completion_(EKEntityTypeReminder, None)
    
    # Get all reminder lists (calendars)
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

def print_reminder_list_details(reminder_list):
    print(f"Title: {reminder_list['title']}")
    print(f"Color: {reminder_list['color']}")
    print(f"Type: {reminder_list['type']}")
    print(f"Allows Content Modifications: {reminder_list['allowsContentModifications']}")
    print(f"UUID: {reminder_list['UUID']}")
    print("------------------------")

# Main execution
if __name__ == "__main__":
    reminder_lists = get_all_reminder_lists()
    
    if reminder_lists:
        print("All Reminder Lists:")
        for reminder_list in reminder_lists:
            print_reminder_list_details(reminder_list)
    else:
        print("No reminder lists found.")