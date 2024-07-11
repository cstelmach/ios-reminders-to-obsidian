from config import config
from datetime_formatter import format_date_for_filename, format_date, format_time, format_datetime
from header_checker import check_section_header_exists
from file_writer import append_reminders, get_header, write_section_header
from datetime import datetime
import os

def write_reminders_to_markdown(reminder_list, completed_reminders):
    folder_path = config['dailyNoteFolderOverwrite'] if config['dailyNoteFolderOverwrite'] else "/default/path/to/your/daily/notes"
    date_format = config['dailyNoteFilenameOverwrite'] if config['dailyNoteFilenameOverwrite'] else "%Y-%m-%d"
    list_header_level = config.get('listHeaderLevel', 3)
    section_header = config.get('sectionHeader', "Completed Tasks")
    section_header_level = config.get('sectionHeaderLevel', 2)
    date_format_for_datetime = config['dateFormat']
    time_format = config['timeFormat']
    separator = config['dateTimeSeparator']
    wrap_in_link = config.get('wrapDateStringInInternalLink', False)

    reminders_by_date = {}
    for reminder in completed_reminders:
        completion_date_str = reminder['completionDate']
        if completion_date_str and completion_date_str != "missing value":
            completion_date = datetime.fromisoformat(completion_date_str).date()
            if completion_date not in reminders_by_date:
                reminders_by_date[completion_date] = []
            reminders_by_date[completion_date].append(reminder)
    
    for date, reminders in reminders_by_date.items():
        formatted_filename_date = format_date_for_filename(date, date_format)
        filename = f"{folder_path}/{formatted_filename_date}.md"
        section_header_exists = check_section_header_exists(filename, section_header, section_header_level)

        with open(filename, 'a') as file:
            if not section_header_exists:
                write_section_header(file, section_header, section_header_level)
            append_reminders(file, reminders, list_header_level, reminder_list, date_format_for_datetime, time_format, separator, wrap_in_link)