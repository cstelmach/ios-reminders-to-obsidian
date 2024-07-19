from datetime import datetime


def group_reminders_by_date(completed_reminders):
    reminders_by_date = {}
    for reminder in completed_reminders:
        completion_date_str = reminder["completionDate"]
        if completion_date_str and completion_date_str != "missing value":
            completion_date = datetime.strptime(
                completion_date_str, "%Y-%m-%d %H:%M:%S"
            ).date()
            if completion_date not in reminders_by_date:
                reminders_by_date[completion_date] = []
            reminders_by_date[completion_date].append(reminder)
    return reminders_by_date
