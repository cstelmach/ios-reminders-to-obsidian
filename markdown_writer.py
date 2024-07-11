from datetime import datetime
from config import config
import os

def format_datetime(date_str):
    if date_str and date_str != "missing value":
        date_obj = datetime.fromisoformat(date_str)
        date_format = config['dateFormat']
        time_format = config['timeFormat']
        separator = config['dateTimeSeparator']
        
        # Format date and time
        formatted_date = date_obj.strftime(date_format.replace('YYYY', '%Y').replace('MM', '%m').replace('DD', '%d'))
        formatted_time = date_obj.strftime(time_format.replace('HH', '%H').replace('mm', '%M').replace('SS', '%S'))
        
        # Combine date and time
        formatted_datetime = f"{formatted_date}{separator}{formatted_time}"
    else:
        formatted_datetime = ""
    return formatted_datetime

def write_reminders_to_markdown(reminder_list, completed_reminders):
    folder_path = config['dailyNoteFolderOverwrite'] if config['dailyNoteFolderOverwrite'] else "/default/path/to/your/daily/notes"
    date_format = config['dailyNoteFilenameOverwrite'] if config['dailyNoteFilenameOverwrite'] else "%Y-%m-%d"

    filename = f"{folder_path}/{reminder_list.replace(' ', '_')}.md"
    with open(filename, 'a') as file:
        for reminder in completed_reminders:
            file.write(f"- [x] {reminder['name']}\n")
            if reminder.get('body') and reminder['body'] != "missing value":
                file.write(f"\t- {reminder['body']}\n")
            if reminder.get('priority') and reminder['priority'] != "0":
                file.write(f"\t- priority: {reminder['priority']}\n")
            if reminder.get('allDayDueDate') and reminder['allDayDueDate'] != "":
                formatted_all_day_due_date = format_datetime(reminder['allDayDueDate'])
                file.write(f"\t- allday due: {formatted_all_day_due_date}\n")
            if reminder.get('dueDate') and reminder['dueDate'] != "":
                formatted_due_date = format_datetime(reminder['dueDate'])
                file.write(f"\t- due: {formatted_due_date}\n")
            formatted_creation_date = format_datetime(reminder['creationDate'])
            file.write(f"\t- created: {formatted_creation_date}\n")
            if reminder.get('completionDate') and reminder['completionDate'] != "":
                formatted_completion_date = format_datetime(reminder['completionDate'])
                file.write(f"\t- completed: {formatted_completion_date}\n")
        file.write("\n")