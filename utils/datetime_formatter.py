# ios_reminders_to_markdown_journal/utils/datetime_formatter.py

from datetime import datetime
from config import config


def format_date(date_input, date_format, wrap_in_link):
    if not date_input or date_input == "missing value":
        return ""

    if isinstance(date_input, str):
        date_obj = datetime.strptime(date_input, "%Y-%m-%d %H:%M:%S")
    elif isinstance(date_input, float):
        date_obj = datetime.fromtimestamp(date_input)
    elif isinstance(date_input, datetime):
        date_obj = date_input
    else:
        raise ValueError(f"Unsupported date format: {type(date_input)}")

    formatted_date = date_obj.strftime(
        date_format.replace("YYYY", "%Y").replace("MM", "%m").replace("DD", "%d")
    )

    if wrap_in_link:
        formatted_date = f"[[{formatted_date}]]"

    return formatted_date


def format_time(date_input, time_format):
    if not date_input or date_input == "missing value":
        return ""

    if isinstance(date_input, str):
        date_obj = datetime.strptime(date_input, "%Y-%m-%d %H:%M:%S")
    elif isinstance(date_input, float):
        date_obj = datetime.fromtimestamp(date_input)
    elif isinstance(date_input, datetime):
        date_obj = date_input
    else:
        raise ValueError(f"Unsupported date format: {type(date_input)}")

    return date_obj.strftime(
        time_format.replace("HH", "%H").replace("mm", "%M").replace("SS", "%S")
    )


def format_datetime(date_str, date_format, time_format, separator, wrap_in_link):
    date_part = format_date(date_str, date_format, False)  # Don't wrap individual parts
    time_part = format_time(date_str, time_format)

    formatted_datetime = f"{date_part}{separator}{time_part}"

    if config.get("makeDatetimesInternalLinkWithAlias", False):
        daily_note_format = config.get("dailyNoteFilenameOverwrite", "YYYY-MM-DD")
        daily_note_date = format_date_for_filename(
            datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"), daily_note_format
        )
        return f"[[{daily_note_date}|{formatted_datetime}]]"
    elif wrap_in_link:
        return f"[[{formatted_datetime}]]"
    else:
        return formatted_datetime


def format_date_for_filename(date_obj, date_format):
    return date_obj.strftime(
        date_format.replace("YYYY", "%Y").replace("MM", "%m").replace("DD", "%d")
    )
