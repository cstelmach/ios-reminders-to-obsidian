from datetime_formatter import format_date, format_time

def get_header(level, text):
    return f"{'#' * level} {text}\n\n"

def append_reminders(file, reminders, list_header_level, reminder_list, date_format_for_datetime, time_format, separator, wrap_in_link):
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