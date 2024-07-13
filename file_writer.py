import os
from datetime import datetime
from config import config
from datetime_formatter import format_date_for_filename
from header_checker import check_section_header_exists
from append_reminders import append_reminders
from reminder_processing import group_reminders_by_date
from file_utils import (
    get_paths_and_template,
    create_file_if_not_exists,
    append_reminders_to_file,
)


def write_reminders_to_markdown(reminder_list, completed_reminders):
    folder_path, date_format, template_path = get_paths_and_template()

    reminders_by_date = group_reminders_by_date(completed_reminders)

    for date, reminders in reminders_by_date.items():
        formatted_filename_date = format_date_for_filename(date, date_format)
        filename = os.path.join(folder_path, f"{formatted_filename_date}.md")
        section_header_exists = check_section_header_exists(
            filename, config["sectionHeader"], config["sectionHeaderLevel"]
        )

        create_file_if_not_exists(filename, template_path)

        append_reminders_to_file(
            filename, reminders, section_header_exists, reminder_list
        )
