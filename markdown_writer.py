from datetime import datetime

def write_reminders_to_markdown(reminder_list, completed_reminders):
    filename = f"{reminder_list.replace(' ', '_')}.md"
    with open(filename, 'a') as file:
        for reminder in completed_reminders:
            file.write(f"- [x] {reminder['name']}\n")
            if reminder.get('body') and reminder['body'] != "missing value":
                file.write(f"\t- {reminder['body']}\n")
            if reminder.get('priority') and reminder['priority'] != "0":
                file.write(f"\t- priority: {reminder['priority']}\n")
            if reminder.get('allDayDueDate') and reminder['allDayDueDate'] != "":
                all_day_due_date = datetime.fromisoformat(reminder['allDayDueDate'])
                file.write(f"\t- allday due: {all_day_due_date.strftime('%d-%m-%Y %H:%M:%S')}\n")
            if reminder.get('dueDate') and reminder['dueDate'] != "":
                due_date = datetime.fromisoformat(reminder['dueDate'])
                file.write(f"\t- due: {due_date.strftime('%d-%m-%Y %H:%M:%S')}\n")
            creation_date = datetime.fromisoformat(reminder['creationDate'])
            file.write(f"\t- created: {creation_date.strftime('%d-%m-%Y %H:%M:%S')}\n")
            if reminder.get('completionDate') and reminder['completionDate'] != "":
                completion_date = datetime.fromisoformat(reminder['completionDate'])
                file.write(f"\t- completed: {completion_date.strftime('%d-%m-%Y %H:%M:%S')}\n")
        file.write("\n")