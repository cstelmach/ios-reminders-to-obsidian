import json
from reminders import (
    get_all_reminder_lists,
    get_completed_reminders_for_list,
    find_parent_reminder,
)
from file_writer import write_reminders_to_markdown


def list_completed_reminders(test_list=None):
    if not test_list:
        print("Getting all reminder lists...")
        reminder_lists = get_all_reminder_lists()
        reminder_lists = [rl["title"] for rl in reminder_lists]
    else:
        reminder_lists = [test_list]

    print("All reminder lists:")
    for reminder_list in reminder_lists:
        print(reminder_list)

    all_completed_reminders = {}
    for reminder_list in reminder_lists:
        print(f"Getting completed reminders for list: {reminder_list}...")
        completed_reminders = get_completed_reminders_for_list(reminder_list)

        # Find parent tasks for subtasks
        for reminder in completed_reminders:
            parent = find_parent_reminder(reminder["UUID"])
            if parent:
                reminder["parent_title"] = parent["title"]
                reminder["parent_completion_date"] = parent["completion_date"]
            else:
                reminder["parent_title"] = None
                reminder["parent_completion_date"] = None

        print(
            f"Raw output for list {reminder_list}: {json.dumps(completed_reminders, indent=2)}"
        )
        all_completed_reminders[reminder_list] = completed_reminders

        # Write to Markdown file
        write_reminders_to_markdown(reminder_list, completed_reminders)

    return all_completed_reminders


if __name__ == "__main__":
    test_list = "temp.crap"
    completed_reminders = list_completed_reminders(test_list=test_list)
    print(json.dumps(completed_reminders, indent=2))
