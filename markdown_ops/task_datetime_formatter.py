# ios_reminders_to_markdown_journal/markdown_ops/task_datetime_formatter.py

from datetime import datetime
from utils.datetime_formatter import format_datetime
from .task_property_formatter import format_property
from config import config


def format_task_dates(
    task, date_format_for_datetime, time_format, separator, wrap_in_link
):
    date_string = ""

    created_string = config.get("createdDateString", "created")
    due_string = config.get("dueDateString", "due")
    completed_string = config.get("completionDateString", "completed")

    # Format creation date if available
    if "creationDate" in task and task["creationDate"]:
        formatted_creation_datetime = format_datetime(
            task["creationDate"],
            date_format_for_datetime,
            time_format,
            separator,
            wrap_in_link,
        )
        date_string += format_property(created_string, formatted_creation_datetime)

    # Format due date if available
    if task.get("dueDate"):
        due_date = datetime.strptime(task["dueDate"], "%Y-%m-%d %H:%M:%S")
        formatted_due_datetime = format_datetime(
            task["dueDate"],
            date_format_for_datetime,
            time_format,
            separator,
            wrap_in_link,
        )

        if task.get("allDayDueDate") or due_date.time() == datetime.min.time():
            due_string = format_property(
                due_string, formatted_due_datetime.split(separator)[0]
            )  # Only use the date part
        else:
            due_string = format_property(due_string, formatted_due_datetime)

        date_string += f", {due_string}" if date_string else due_string

    # Format completion date if available
    if "completionDate" in task and task["completionDate"]:
        formatted_completion_datetime = format_datetime(
            task["completionDate"],
            date_format_for_datetime,
            time_format,
            separator,
            wrap_in_link,
        )
        completion_string = format_property(
            completed_string, formatted_completion_datetime
        )
        date_string += f" -> {completion_string}" if date_string else completion_string

    return date_string
