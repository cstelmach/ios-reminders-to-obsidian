from datetime import datetime
from config import config
import os

def format_date(date_str, date_format, wrap_in_link):
    if date_str and date_str != "missing value":
        date_obj = datetime.fromisoformat(date_str)
        formatted_date = date_obj.strftime(date_format.replace('YYYY', '%Y').replace('MM', '%m').replace('DD', '%d'))
        
        if wrap_in_link:
            formatted_date = f"[[{formatted_date}]]"
    else:
        formatted_date = ""
    return formatted_date

def format_time(date_str, time_format):
    if date_str and date_str != "missing value":
        date_obj = datetime.fromisoformat(date_str)
        formatted_time = date_obj.strftime(time_format.replace('HH', '%H').replace('mm', '%M').replace('SS', '%S'))
    else:
        formatted_time = ""
    return formatted_time

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
                file.write(get_header(section_header_level, section_header))
            file.write(get_header(list_header_level, reminder_list))
            for reminder in reminders:
                file.write(f"- [x] {reminder['name']}\n")
                if reminder.get('body') and reminder['body'] != "missing value":
                    file.write(f"\t- {reminder['body']}\n")
                if reminder.get('priority') and reminder['priority'] != "0":
                    file.write(f"\t- priority: {reminder['priority']}\n")
                if reminder.get('allDayDueDate') and reminder['allDayDueDate'] != "":
                    formatted_all_day_due_date = format_date(reminder['allDayDueDate'], date_format_for_datetime, wrap_in_link)
                    file.write(f"\t- allday due: {formatted_all_day_due_date}\n")
                if reminder.get('dueDate') and reminder['dueDate'] != "":
                    formatted_due_date = format_date(reminder['dueDate'], date_format_for_datetime, wrap_in_link)
                    formatted_due_time = format_time(reminder['dueDate'], time_format)
                    file.write(f"\t- due: {formatted_due_date} {formatted_due_time}\n")
                formatted_creation_date = format_date(reminder['creationDate'], date_format_for_datetime, wrap_in_link)
                formatted_creation_time = format_time(reminder['creationDate'], time_format)
                file.write(f"\t- created: {formatted_creation_date} {formatted_creation_time}\n")
                if reminder.get('completionDate') and reminder['completionDate'] != "":
                    formatted_completion_date = format_date(reminder['completionDate'], date_format_for_datetime, wrap_in_link)
                    formatted_completion_time = format_time(reminder['completionDate'], time_format)
                    file.write(f"\t- completed: {formatted_completion_date} {formatted_completion_time}\n")
            file.write("\n")