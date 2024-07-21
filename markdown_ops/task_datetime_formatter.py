# ios_reminders_to_markdown_journal/markdown_ops/task_datetime_formatter.py

from datetime import datetime
from utils.datetime_formatter import format_date, format_time
from .task_property_formatter import format_property
from config import config


def format_task_dates(task, date_format_for_datetime, time_format, wrap_in_link):
    date_string = ""

    created_string = config.get("createdDateString", "created")
    due_string = config.get("dueDateString", "due")
    completed_string = config.get("completionDateString", "completion")

    # Format creation date if available
    if "creationDate" in task and task["creationDate"]:
        formatted_creation_date = format_date(
            task["creationDate"], date_format_for_datetime, wrap_in_link
        )
        formatted_creation_time = format_time(task["creationDate"], time_format)
        date_string += format_property(
            created_string, f"{formatted_creation_date} {formatted_creation_time}"
        )

    # Format due date if available
    if task.get("dueDate"):
        due_date = datetime.strptime(task["dueDate"], "%Y-%m-%d %H:%M:%S")
        formatted_due_date = format_date(
            task["dueDate"], date_format_for_datetime, wrap_in_link
        )

        if task.get("allDayDueDate") or due_date.time() == datetime.min.time():
            due_string = format_property(due_string, formatted_due_date)
        else:
            formatted_due_time = format_time(task["dueDate"], time_format)
            due_string = format_property(
                due_string, f"{formatted_due_date} {formatted_due_time}"
            )

        date_string += f", {due_string}" if date_string else due_string

    # Format completion date if available
    if "completionDate" in task and task["completionDate"]:
        formatted_completion_date = format_date(
            task["completionDate"], date_format_for_datetime, wrap_in_link
        )
        formatted_completion_time = format_time(task["completionDate"], time_format)
        completion_string = format_property(
            completed_string, f"{formatted_completion_date} {formatted_completion_time}"
        )
        date_string += f" -> {completion_string}" if date_string else completion_string

    return date_string
