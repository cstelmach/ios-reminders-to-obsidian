from datetime import datetime
from config import config
import os

def format_datetime(date_str, date_format, time_format, separator):
    if date_str and date_str != "missing value":
        date_obj = datetime.fromisoformat(date_str)
        formatted_date = date_obj.strftime(date_format.replace('YYYY', '%Y').replace('MM', '%m').replace('DD', '%d'))
        formatted_time = date_obj.strftime(time_format.replace('HH', '%H').replace('mm', '%M').replace('SS', '%S'))
        formatted_datetime = f"{formatted_date}{separator}{formatted_time}"
    else:
        formatted_datetime = ""
    return formatted_datetime

def format_date_for_filename(date_obj, date_format):
    return date_obj.strftime(date_format.replace('YYYY', '%Y').replace('MM', '%m').replace('DD', '%d'))

def get_header(level, text):
    return f"{'#' * level} {text}\n\n"

def check_section_header_exists(filepath, section_header, section_header_level):
    if not os.path.exists(filepath):
        return False
    with open(filepath, 'r') as file:
        content = file.read()
    header = f"\n{'#' * section_header_level} {section_header}\n"
    return header in content

def write_reminders_to_markdown(reminder_list, completed_reminders):
    folder_path = config['dailyNoteFolderOverwrite'] if config['dailyNoteFolderOverwrite'] else "/default/path/to/your/daily/notes"
    date_format = config['dailyNoteFilenameOverwrite'] if config['dailyNoteFilenameOverwrite'] else "%Y-%m-%d"
    list_header_level = config.get('listHeaderLevel', 3)
    section_header = config.get('sectionHeader', "Completed Tasks")
    section_header_level = config.get('sectionHeaderLevel', 2)
    date_format_for_datetime = config['dateFormat']
    time_format = config['timeFormat']
    separator = config['dateTimeSeparator']

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
                file.write(get_header(section_header_level, section_header))
            file.write(get_header(list_header_level, reminder_list))
            for reminder in reminders:
                file.write(f"- [x] {reminder['name']}\n")
                if reminder.get('body') and reminder['body'] != "missing value":
                    file.write(f"\t- {reminder['body']}\n")
                if reminder.get('priority') and reminder['priority'] != "0":
                    file.write(f"\t- priority: {reminder['priority']}\n")
                if reminder.get('allDayDueDate') and reminder['allDayDueDate'] != "":
                    formatted_all_day_due_date = format_datetime(reminder['allDayDueDate'], date_format_for_datetime, time_format, separator)
                    file.write(f"\t- allday due: {formatted_all_day_due_date}\n")
                if reminder.get('dueDate') and reminder['dueDate'] != "":
                    formatted_due_date = format_datetime(reminder['dueDate'], date_format_for_datetime, time_format, separator)
                    file.write(f"\t- due: {formatted_due_date}\n")
                formatted_creation_date = format_datetime(reminder['creationDate'], date_format_for_datetime, time_format, separator)
                file.write(f"\t- created: {formatted_creation_date}\n")
                if reminder.get('completionDate') and reminder['completionDate'] != "":
                    formatted_completion_date = format_datetime(reminder['completionDate'], date_format_for_datetime, time_format, separator)
                    file.write(f"\t- completed: {formatted_completion_date}\n")
            file.write("\n")