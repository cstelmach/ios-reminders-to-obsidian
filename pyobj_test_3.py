from Foundation import NSDate
from EventKit import EKEventStore, EKReminder, EKEntityTypeReminder

def get_reminders_from_list(list_name):
    store = EKEventStore.alloc().init()
    store.requestAccessToEntityType_completion_(EKEntityTypeReminder, None)
    
    calendars = store.calendarsForEntityType_(EKEntityTypeReminder)
    target_calendar = next((calendar for calendar in calendars if calendar.title() == list_name), None)
    
    if not target_calendar:
        print(f"List '{list_name}' not found.")
        return []
    
    predicate = store.predicateForRemindersInCalendars_([target_calendar])
    reminders = store.remindersMatchingPredicate_(predicate)
    
    return reminders

def identify_parent_child_relationships(reminders):
    relationships = {}
    current_parent = None
    indent_level = 0

    for reminder in reminders:
        title = reminder.title()
        print(title)
        if title.startswith('-'):
            indent = len(title) - len(title.lstrip('-'))
            clean_title = title.lstrip('- ')
            
            if indent > indent_level:
                current_parent = relationships.get('parents', [])[-1] if relationships.get('parents') else None
                indent_level = indent
            elif indent < indent_level:
                current_parent = None
                indent_level = indent
            
            if current_parent:
                if 'children' not in relationships:
                    relationships['children'] = []
                relationships['children'].append((clean_title, current_parent))
            else:
                if 'parents' not in relationships:
                    relationships['parents'] = []
                relationships['parents'].append(clean_title)

    return relationships

def print_relationships(relationships):
    print("Parent Reminders:")
    for parent in relationships.get('parents', []):
        print(f"- {parent}")
    
    print("\nChild Reminders:")
    for child, parent in relationships.get('children', []):
        print(f"- {child} (Parent: {parent})")

if __name__ == "__main__":
    list_name = "temp.crap"
    reminders = get_reminders_from_list(list_name)
    
    if reminders:
        print(f"Analyzing reminders in the list '{list_name}':")
        relationships = identify_parent_child_relationships(reminders)
        print_relationships(relationships)
    else:
        print(f"No reminders found in the list '{list_name}'.")