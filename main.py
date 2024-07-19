import re
from config import config
from utils import get_date_range, update_cache
from reminders import (
    get_all_reminder_lists,
    get_completed_reminders_for_list,
    find_parent_reminder,
)
from markdown_ops import write_reminders_to_markdown


def list_completed_reminders(test_lists=None):
    if not test_lists:
        print("Getting all reminder lists...")
        all_reminder_lists = get_all_reminder_lists()
        reminder_lists = filter_reminder_lists(all_reminder_lists)
    else:
        if isinstance(test_lists, str):
            test_lists = [test_lists]
        reminder_lists = test_lists

    print("Reminder lists to import:")
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


def filter_reminder_lists(all_reminder_lists):
    lists_to_import = config.get("listsToImport", [])

    if not lists_to_import:
        return []

    filtered_lists = []
    for reminder_list in all_reminder_lists:
        list_title = reminder_list["title"]
        for list_filter in lists_to_import:
            if isinstance(list_filter, str):
                if list_filter == list_title:
                    filtered_lists.append(list_title)
                    break
            elif hasattr(list_filter, "match"):  # Check if it's a regex object
                if list_filter.match(list_title):
                    filtered_lists.append(list_title)
                    break
            else:
                try:
                    if re.match(list_filter, list_title):
                        filtered_lists.append(list_title)
                        break
                except re.error:
                    print(f"Invalid regex pattern: {list_filter}")

    return filtered_lists


if __name__ == "__main__":
    completed_reminders = list_completed_reminders()
