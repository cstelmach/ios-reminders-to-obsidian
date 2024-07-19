from datetime import datetime
from utils.datetime_formatter import format_date, format_time
from config import config


def format_datetime(key, date, time, use_metadata_formatting):
    if use_metadata_formatting:
        return f"[{key}:: {date} {time}]"
    else:
        return f"{key}: {date} {time}"


def format_task_dates(task, date_format_for_datetime, time_format, wrap_in_link):
    use_metadata_formatting = config.get("useMetadataFormattingForDatetimes", False)

    formatted_creation_date = format_date(
        task["creationDate"], date_format_for_datetime, wrap_in_link
    )
    formatted_creation_time = format_time(task["creationDate"], time_format)

    formatted_completion_date = format_date(
        task["completionDate"], date_format_for_datetime, wrap_in_link
    )
    formatted_completion_time = format_time(task["completionDate"], time_format)

    date_string = format_datetime(
        "created",
        formatted_creation_date,
        formatted_creation_time,
        use_metadata_formatting,
    )

    if task.get("dueDate"):
        due_date = datetime.strptime(task["dueDate"], "%Y-%m-%d %H:%M:%S")
        formatted_due_date = format_date(
            task["dueDate"], date_format_for_datetime, wrap_in_link
        )

        if task.get("allDayDueDate") or due_date.time() == datetime.min.time():
            due_string = format_datetime(
                "due", formatted_due_date, "", use_metadata_formatting
            )
        else:
            formatted_due_time = format_time(task["dueDate"], time_format)
            due_string = format_datetime(
                "due", formatted_due_date, formatted_due_time, use_metadata_formatting
            )

        date_string += f", {due_string}"

    completion_string = format_datetime(
        "completed",
        formatted_completion_date,
        formatted_completion_time,
        use_metadata_formatting,
    )
    date_string += f" -> {completion_string}"

    return date_string
