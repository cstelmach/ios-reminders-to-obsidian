from datetime import datetime


def format_date(date_input, date_format, wrap_in_link):
    if not date_input or date_input == "missing value":
        return ""

    if isinstance(date_input, str):
        try:
            date_obj = datetime.fromisoformat(date_input)
        except ValueError:
            # If it's not ISO format, try parsing it as a timestamp
            date_obj = datetime.fromtimestamp(float(date_input))
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
        try:
            date_obj = datetime.fromisoformat(date_input)
        except ValueError:
            # If it's not ISO format, try parsing it as a timestamp
            date_obj = datetime.fromtimestamp(float(date_input))
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
    date_part = format_date(date_str, date_format, wrap_in_link)
    time_part = format_time(date_str, time_format)
    if date_part and time_part:
        return f"{date_part}{separator}{time_part}"
    return date_part


def format_date_for_filename(date_obj, date_format):
    return date_obj.strftime(
        date_format.replace("YYYY", "%Y").replace("MM", "%m").replace("DD", "%d")
    )
