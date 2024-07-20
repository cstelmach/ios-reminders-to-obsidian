import os
from config import config
from utils.datetime_formatter import format_date_for_filename
from .file_utils import get_paths_and_template, create_file_if_not_exists
from .header_utils import check_export_header_exists
from .reminder_grouping import group_reminders_by_date
from .reminder_writer import append_reminders_to_file


def write_reminders_to_markdown(reminder_list, completed_reminders):
    folder_path, date_format, template_path = get_paths_and_template()

    reminders_by_date = group_reminders_by_date(completed_reminders)

    for date, reminders in reminders_by_date.items():
        formatted_filename_date = format_date_for_filename(date, date_format)
        filename = os.path.join(folder_path, f"{formatted_filename_date}.md")
        export_header_exists = check_export_header_exists(
            filename, config["exportHeader"], config["exportHeaderLevel"]
        )

        if config["skipNotesAlreadyImported"] and export_header_exists:
            print(
                f"Skipping {filename} as it already contains the completed tasks header."
            )
            continue

        create_file_if_not_exists(filename, template_path)

        append_reminders_to_file(
            filename, reminders, export_header_exists, reminder_list, config
        )
