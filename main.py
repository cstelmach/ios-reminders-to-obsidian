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
    import_but_all_overwrite = config.get("importButAllOverwrite", False)
    lists_to_import = config.get("listsToImport", [])
    lists_to_omit = config.get("listsToOmit", [])

    filtered_lists = []
    for reminder_list in all_reminder_lists:
        list_title = reminder_list["title"]

        # Check if the list should be omitted
        if should_omit_list(list_title, lists_to_omit):
            continue

        # If importButAllOverwrite is True, include all lists except those in listsToOmit
        if import_but_all_overwrite:
            filtered_lists.append(list_title)
        # Otherwise, only include lists specified in listsToImport
        elif should_import_list(list_title, lists_to_import):
            filtered_lists.append(list_title)

    return filtered_lists


def should_omit_list(list_title, lists_to_omit):
    return any(match_pattern(list_title, pattern) for pattern in lists_to_omit)


def should_import_list(list_title, lists_to_import):
    return any(match_pattern(list_title, pattern) for pattern in lists_to_import)


def match_pattern(list_title, pattern):
    if isinstance(pattern, str):
        return pattern == list_title
    elif hasattr(pattern, "match"):  # Check if it's a regex object
        return pattern.match(list_title)
    else:
        try:
            return re.match(pattern, list_title)
        except re.error:
            print(f"Invalid regex pattern: {pattern}")
            return False


if __name__ == "__main__":
    completed_reminders = list_completed_reminders()
