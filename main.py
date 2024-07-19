import json
from config import config
from reminders import (
    get_all_reminder_lists,
    get_completed_reminders_for_list,
    find_parent_reminder,
)
from file_writer import write_reminders_to_markdown
from utils import get_date_range, update_cache


def list_completed_reminders(test_lists=None):
    if not test_lists:
        print("Getting all reminder lists...")
        reminder_lists = get_all_reminder_lists()
        reminder_lists = [rl["title"] for rl in reminder_lists]
    else:
        # if test_lists is a string, make it a list
        if isinstance(test_lists, str):
            test_lists = [test_lists]
        reminder_lists = test_lists

    print("All reminder lists:")
    for reminder_list in reminder_lists:
        print(reminder_list)

    start_date, end_date = get_date_range()

    all_completed_reminders = {}
    for reminder_list in reminder_lists:
        print(f"Getting completed reminders for list: {reminder_list}...")
        completed_reminders = get_completed_reminders_for_list(
            reminder_list, start_date, end_date
        )

        # Find parent tasks for subtasks
        for reminder in completed_reminders:
            parent = find_parent_reminder(reminder["UUID"])
            if parent:
                reminder["parent_title"] = parent.get("title", "No title")
                reminder["parent_uuid"] = parent.get("uuid")
            else:
                reminder["parent_title"] = None
                reminder["parent_uuid"] = None

        all_completed_reminders[reminder_list] = completed_reminders

        # Write to Markdown file
        write_reminders_to_markdown(reminder_list, completed_reminders)

    if config["isCacheActive"]:
        update_cache()

    return all_completed_reminders


if __name__ == "__main__":
    test_lists = ["temp.crap", "temp.mayfly"]
    completed_reminders = list_completed_reminders(test_lists=test_lists)
