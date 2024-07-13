from datetime_formatter import format_date, format_time
from indentation_utils import write_multiline_text, write_multiline_body
from subtasks_utils import append_subtasks
from header_utils import get_header
from datetime import datetime, timedelta


def append_reminders(
    file,
    reminders,
    list_header_level,
    reminder_list,
    date_format_for_datetime,
    time_format,
    separator,
    wrap_in_link,
):
    file.write(get_header(list_header_level, reminder_list))

    parent_tasks = {}
    child_tasks = []

    for reminder in reminders:
        if reminder.get("parent_title"):
            parent_key = (
                reminder["parent_title"],
                reminder.get("parent_completion_date"),
            )
            if parent_key not in parent_tasks:
                parent_tasks[parent_key] = []
            parent_tasks[parent_key].append(reminder)
        else:
            child_tasks.append(reminder)

    for reminder in child_tasks:
        if reminder.get("name") and reminder["name"] != "missing value":
            write_multiline_text(file, reminder["name"])
            if reminder.get("body") and reminder["body"] != "missing value":
                write_multiline_body(file, reminder["body"], prefix="\t")
            if reminder.get("priority") and reminder["priority"] != 0:
                file.write(f"\t- priority: {reminder['priority']}\n")

            formatted_creation_date = format_date(
                reminder["creationDate"], date_format_for_datetime, wrap_in_link
            )
            formatted_creation_time = format_time(reminder["creationDate"], time_format)
            formatted_completion_date = format_date(
                reminder["completionDate"], date_format_for_datetime, wrap_in_link
            )
            formatted_completion_time = format_time(
                reminder["completionDate"], time_format
            )

            file.write(
                f"\t- created: {formatted_creation_date} {formatted_creation_time} -> completed: {formatted_completion_date} {formatted_completion_time}\n"
            )
            file.write("\n")

    for (parent_title, parent_completion_date), subtasks in parent_tasks.items():
        parent_completed = (
            all(
                compare_dates(subtask["completionDate"], parent_completion_date)
                for subtask in subtasks
            )
            if parent_completion_date
            else False
        )

        parent_checkbox = "[x]" if parent_completed else "[-]"
        write_multiline_text(
            file, parent_title, prefix="", initial_prefix=f"- {parent_checkbox} "
        )

        if parent_completed:
            formatted_completion_date = format_date(
                parent_completion_date, date_format_for_datetime, wrap_in_link
            )
            formatted_completion_time = format_time(parent_completion_date, time_format)
            file.write(
                f"\t- completed: {formatted_completion_date} {formatted_completion_time}\n"
            )

        append_subtasks(
            file,
            subtasks,
            date_format_for_datetime,
            time_format,
            separator,
            wrap_in_link,
            "\t",
        )
        file.write("\n")


def compare_dates(date1, date2):
    print(f"date1: {date1}, date2: {date2}")
    if not date1 or not date2:
        return False

    def parse_date(date_input):
        if isinstance(date_input, str):
            return datetime.strptime(date_input, "%Y-%m-%d %H:%M:%S %z").date()
        elif isinstance(date_input, float):
            cocoa_reference_date = datetime(2001, 1, 1)
            return (cocoa_reference_date + timedelta(seconds=date_input)).date()
        else:
            raise ValueError(f"Unsupported date format: {type(date_input)}")

    date1_obj = parse_date(date1)
    date2_obj = parse_date(date2)
    print(f"date1_obj: {date1_obj}, date2_obj: {date2_obj}")
    return date1_obj == date2_obj
