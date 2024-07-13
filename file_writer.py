import os
import json
from config import config
from datetime_formatter import format_date_for_filename
from header_checker import check_section_header_exists
from header_utils import write_section_header
from reminders_utils import append_reminders
from datetime import datetime


def write_reminders_to_markdown(reminder_list, completed_reminders):
    folder_path = (
        config["dailyNoteFolderOverwrite"]
        if config["dailyNoteFolderOverwrite"]
        else None
    )
    date_format = (
        config["dailyNoteFilenameOverwrite"]
        if config["dailyNoteFilenameOverwrite"]
        else None
    )
    list_header_level = config.get("listHeaderLevel", 3)
    section_header = config.get("sectionHeader", "Completed Tasks")
    section_header_level = config.get("sectionHeaderLevel", 2)
    date_format_for_datetime = config["dateFormat"]
    time_format = config["timeFormat"]
    separator = config["dateTimeSeparator"]
    wrap_in_link = config.get("wrapDateStringInInternalLink", False)
    template_path = config["templateOverwritePath"]

    if not folder_path or not date_format:
        obsidian_parent_path = os.path.dirname(config["obsidianSettingsPath"])
        periodic_notes_config_path = os.path.join(
            obsidian_parent_path, "plugins/periodic-notes/data.json"
        )
        with open(periodic_notes_config_path, "r") as file:
            periodic_notes_config = json.load(file)
            daily_config = periodic_notes_config.get("daily", {})
            if not folder_path:
                folder_path = os.path.join(
                    obsidian_parent_path, daily_config.get("folder")
                )
            if not date_format:
                date_format = daily_config.get("format")
            if not template_path:
                template_path = os.path.join(
                    obsidian_parent_path, daily_config.get("template")
                )

    reminders_by_date = {}
    for reminder in completed_reminders:
        completion_date_str = reminder["completionDate"]
        if completion_date_str and completion_date_str != "missing value":
            completion_date = datetime.strptime(
                completion_date_str, "%Y-%m-%d %H:%M:%S %z"
            ).date()
            if completion_date not in reminders_by_date:
                reminders_by_date[completion_date] = []
            reminders_by_date[completion_date].append(reminder)

    for date, reminders in reminders_by_date.items():
        formatted_filename_date = format_date_for_filename(date, date_format)
        filename = os.path.join(folder_path, f"{formatted_filename_date}.md")
        section_header_exists = check_section_header_exists(
            filename, section_header, section_header_level
        )

        if not os.path.exists(filename):
            with open(filename, "w") as file:
                if template_path and os.path.exists(template_path):
                    with open(template_path, "r") as template_file:
                        file.write(template_file.read())
                else:
                    file.write("\n\n")
        
        # Append reminders to the daily note
        with open(filename, "a") as file:
            if not section_header_exists:
                write_section_header(file, section_header, section_header_level)
            else:
                file.write("\n")
            append_reminders(
                file,
                reminders,
                list_header_level,
                reminder_list,
                date_format_for_datetime,
                time_format,
                separator,
                wrap_in_link,
            )
