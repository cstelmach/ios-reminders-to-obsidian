import os
from datetime import datetime
from config import config
from utils.datetime_formatter import format_date_for_filename
from .header_utils import check_section_header_exists, write_section_header, get_header
from .file_utils import get_paths_and_template, create_file_if_not_exists
from processing.task_processing import (
    separate_tasks,
    group_child_tasks_by_parent,
    process_main_tasks,
    process_child_tasks_without_parent,
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

        if config["skipNotesAlreadyImported"] and section_header_exists:
            print(
                f"Skipping {filename} as it already contains the completed tasks header."
            )
            continue

        create_file_if_not_exists(filename, template_path)

        append_reminders_to_file(
            filename, reminders, section_header_exists, reminder_list
        )


def group_reminders_by_date(completed_reminders):
    reminders_by_date = {}
    for reminder in completed_reminders:
        completion_date_str = reminder["completionDate"]
        if completion_date_str and completion_date_str != "missing value":
            completion_date = datetime.strptime(completion_date_str, "%Y-%m-%d").date()
            if completion_date not in reminders_by_date:
                reminders_by_date[completion_date] = []
            reminders_by_date[completion_date].append(reminder)
    return reminders_by_date


def append_reminders_to_file(filename, reminders, section_header_exists, reminder_list):
    with open(filename, "a") as file:
        if not section_header_exists:
            write_section_header(
                file, config["sectionHeader"], config["sectionHeaderLevel"]
            )
        else:
            file.write("\n")
        append_reminders(
            file,
            reminders,
            config.get("listHeaderLevel", 3),
            reminder_list,
            config["dateFormat"],
            config["timeFormat"],
            config["dateTimeSeparator"],
            config.get("wrapDateStringInInternalLink", False),
        )


def append_reminders(
    file,
    reminders,
    list_header_level,
    reminder_list,
    date_format_for_datetime,
    time_format,
    separator,
    wrap_in_link,
):
    file.write(get_header(list_header_level, reminder_list))

    main_tasks, child_tasks = separate_tasks(reminders)
    child_tasks_by_parent_uuid = group_child_tasks_by_parent(child_tasks)

    process_main_tasks(
        file,
        main_tasks,
        child_tasks_by_parent_uuid,
        date_format_for_datetime,
        time_format,
        separator,
        wrap_in_link,
    )
    process_child_tasks_without_parent(
        file,
        child_tasks_by_parent_uuid,
        main_tasks,
        date_format_for_datetime,
        time_format,
        separator,
        wrap_in_link,
    )
