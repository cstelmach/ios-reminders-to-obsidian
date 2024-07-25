import json
import os
from datetime import datetime
from config import config


def export_reminders_to_json(completed_reminders):
    if not config["exportToJSON"]:
        return

    json_folder_path = config["jsonExportFolderPath"]
    if not json_folder_path:
        raise ValueError("JSON export folder path is not defined in the configuration.")

    os.makedirs(json_folder_path, exist_ok=True)

    reminders_by_date = group_reminders_by_date(completed_reminders)

    for date, reminders in reminders_by_date.items():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file_path = os.path.join(
            json_folder_path, f"{date.strftime('%Y-%m-%d')}_{timestamp}.json"
        )

        try:
            with open(json_file_path, "w", encoding="utf-8") as file:
                json.dump(reminders, file, ensure_ascii=False, indent=2, default=str)

            print(f"Successfully exported JSON to {json_file_path}")
        except Exception as e:
            print(f"Error exporting JSON for {date}: {e}")


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
