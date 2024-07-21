# ios_reminders_to_markdown_journal/markdown_ops/task_datetime_formatter.py

from datetime import datetime
from utils.datetime_formatter import (
    format_datetime,
    format_date,
    format_date_for_filename,
)
from .task_property_formatter import format_property
from config import config


def format_task_dates(
    task, date_format_for_datetime, time_format, separator, wrap_in_link
):
    date_string = ""

    created_string = config.get("createdDateString", "created")
    due_string = config.get("dueDateString", "due")
    completed_string = config.get("completionDateString", "completed")

    makeDatetimesInternalLinkWithAlias = config.get(
        "makeDatetimesInternalLinkWithAlias", False
    )
    daily_note_format = config.get("dailyNoteFilenameOverwrite", "YYYY-MM-DD")

    # Format creation date if available
    if "creationDate" in task and task["creationDate"]:
        formatted_creation_datetime = format_datetime(
            task["creationDate"],
            date_format_for_datetime,
            time_format,
            separator,
            makeDatetimesInternalLinkWithAlias or wrap_in_link,
        )
        date_string += format_property(created_string, formatted_creation_datetime)

    # Format due date if available
    if task.get("dueDate"):
        due_date = datetime.strptime(task["dueDate"], "%Y-%m-%d %H:%M:%S")
        if task.get("allDayDueDate") or due_date.time() == datetime.min.time():
            # For all-day due dates, only use the date part
            formatted_due_date = format_date(due_date, date_format_for_datetime, False)
            if makeDatetimesInternalLinkWithAlias:
                daily_note_date = format_date_for_filename(due_date, daily_note_format)
                formatted_due_date = f"[[{daily_note_date}|{formatted_due_date}]]"
            elif wrap_in_link:
                formatted_due_date = f"[[{formatted_due_date}]]"
            due_string = format_property(due_string, formatted_due_date)
        else:
            formatted_due_datetime = format_datetime(
                task["dueDate"],
                date_format_for_datetime,
                time_format,
                separator,
                makeDatetimesInternalLinkWithAlias or wrap_in_link,
            )
            due_string = format_property(due_string, formatted_due_datetime)

        date_string += f", {due_string}" if date_string else due_string

    # Format completion date if available
    if "completionDate" in task and task["completionDate"]:
        formatted_completion_datetime = format_datetime(
            task["completionDate"],
            date_format_for_datetime,
            time_format,
            separator,
            makeDatetimesInternalLinkWithAlias or wrap_in_link,
        )
        completion_string = format_property(
            completed_string, formatted_completion_datetime
        )
        date_string += f" -> {completion_string}" if date_string else completion_string

    return date_string
