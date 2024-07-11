from datetime import datetime

def write_reminders_to_markdown(reminder_list, completed_reminders):
    filename = f"{reminder_list.replace(' ', '_')}.md"
    with open(filename, 'a') as file:
        for reminder in completed_reminders:
            file.write(f"- [x] {reminder['title']}\n")
            if reminder.get('note'):
                file.write(f"\t- {reminder['note']}\n")
            completed_date = datetime.fromisoformat(reminder['completedDate'])
            file.write(f"\t- completed: {completed_date.strftime('%d-%m-%Y %H:%M:%S')}\n")
        file.write("\n")
    # Debug: Print the filepath
    print(f"Markdown file written to: {filename}")