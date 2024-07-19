from datetime import datetime
from utils.datetime_formatter import format_date, format_time
from .task_property_formatter import format_property


def format_task_dates(task, date_format_for_datetime, time_format, wrap_in_link):
    formatted_creation_date = format_date(
        task["creationDate"], date_format_for_datetime, wrap_in_link
    )
    formatted_creation_time = format_time(task["creationDate"], time_format)

    formatted_completion_date = format_date(
        task["completionDate"], date_format_for_datetime, wrap_in_link
    )
    formatted_completion_time = format_time(task["completionDate"], time_format)

    date_string = format_property(
        "created", f"{formatted_creation_date} {formatted_creation_time}"
    )

    if task.get("dueDate"):
        due_date = datetime.strptime(task["dueDate"], "%Y-%m-%d %H:%M:%S")
        formatted_due_date = format_date(
            task["dueDate"], date_format_for_datetime, wrap_in_link
        )

        if task.get("allDayDueDate") or due_date.time() == datetime.min.time():
            due_string = format_property("due", formatted_due_date)
        else:
            formatted_due_time = format_time(task["dueDate"], time_format)
            due_string = format_property(
                "due", f"{formatted_due_date} {formatted_due_time}"
            )

        date_string += f", {due_string}"

    completion_string = format_property(
        "completed", f"{formatted_completion_date} {formatted_completion_time}"
    )
    date_string += f" -> {completion_string}"

    return date_string
