# python_modules/ios_reminders_to_markdown_journal/main.py

from config import config, get_date_range, update_cache
from reminders import (
    get_all_reminder_lists,
    get_completed_reminders_for_list,
    filter_reminder_lists,
)
from markdown_ops import write_reminders_to_markdown
from csv_export import export_reminders_to_csv
from json_export import export_reminders_to_json


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

    print(
        f"Getting completed reminders for all lists from {start_date} to {end_date}..."
    )
    all_completed_reminders = get_completed_reminders_for_list(
        reminder_lists, start_date, end_date
    )

    for reminder_list, completed_reminders in all_completed_reminders.items():
        print(f"Processing completed reminders for list: {reminder_list}...")

        # Write to Markdown file
        write_reminders_to_markdown(reminder_list, completed_reminders)

        # Export to CSV if enabled
        if config.get("exportToCSV", False):
            export_reminders_to_csv(completed_reminders)

        # Export to JSON if enabled
        if config.get("exportToJSON", False):
            export_reminders_to_json(completed_reminders)

    update_cache()

    print("Completed reminders processed successfully")

    return all_completed_reminders


if __name__ == "__main__":
    completed_reminders = list_completed_reminders()


    # execute via command line, command:
    # /opt/homebrew/Caskroom/miniconda/base/bin/python3 /Users/cs/local/code/applications_large/ios_reminders_to_markdown_journal/main.py
