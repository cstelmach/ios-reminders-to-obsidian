import csv
import os
from datetime import datetime
from config import config


def export_reminders_to_csv(completed_reminders):
    if not config["exportToCSV"]:
        return

    csv_folder_path = config["csvExportFolderPath"]
    if not csv_folder_path:
        raise ValueError("CSV export folder path is not defined in the configuration.")

    os.makedirs(csv_folder_path, exist_ok=True)

    reminders_by_date = group_reminders_by_date(completed_reminders)

    for date, reminders in reminders_by_date.items():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file_path = os.path.join(
            csv_folder_path, f"{date.strftime('%Y-%m-%d')}_{timestamp}.csv"
        )

        try:
            with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = get_fieldnames(reminders)
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for reminder in reminders:
                    writer.writerow(format_reminder_for_csv(reminder))

            print(f"Successfully exported CSV to {csv_file_path}")
        except Exception as e:
            print(f"Error exporting CSV for {date}: {e}")


def group_reminders_by_date(completed_reminders):
    reminders_by_date = {}
    for reminder in completed_reminders:
        completion_date = reminder.get("completionDate")
        if completion_date:
            try:
                completion_date = datetime.strptime(
                    completion_date, "%Y-%m-%d %H:%M:%S"
                ).date()
            except ValueError:
                print(
                    f"Warning: Invalid completion date format for reminder: {reminder['name']}"
                )
                continue
        else:
            # Use creation date if completion date is not available
            creation_date = reminder.get("creationDate")
            if creation_date:
                try:
                    completion_date = datetime.strptime(
                        creation_date, "%Y-%m-%d %H:%M:%S"
                    ).date()
                except ValueError:
                    print(
                        f"Warning: Invalid creation date format for reminder: {reminder['name']}"
                    )
                    continue
            else:
                print(f"Warning: No valid date found for reminder: {reminder['name']}")
                continue

        if completion_date not in reminders_by_date:
            reminders_by_date[completion_date] = []
        reminders_by_date[completion_date].append(reminder)
    return reminders_by_date


def get_fieldnames(reminders):
    fieldnames = set()
    for reminder in reminders:
        fieldnames.update(reminder.keys())
    return sorted(list(fieldnames))


def format_reminder_for_csv(reminder):
    formatted_reminder = reminder.copy()

    # Convert list of tags to a comma-separated string
    if "tags" in formatted_reminder:
        formatted_reminder["tags"] = ", ".join(formatted_reminder["tags"])

    # Convert any complex data types to strings
    for key, value in formatted_reminder.items():
        if not isinstance(value, (str, int, float, bool, type(None))):
            formatted_reminder[key] = str(value)

    return formatted_reminder
